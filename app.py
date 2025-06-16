import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from forms import CreateLinksetForm, CaptchaForm
from models import LinksetStorage
from utils import generate_slug, validate_urls
import requests
import json
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize storage
storage = LinksetStorage()

# reCAPTCHA configuration
RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI")  # Test key
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY", "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe")  # Test key

def verify_recaptcha(response_token):
    """Verify reCAPTCHA response"""
    try:
        payload = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': response_token
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload, timeout=10)
        result = response.json()
        return result.get('success', False)
    except Exception as e:
        logging.error(f"reCAPTCHA verification error: {e}")
        return False

@app.route('/')
def index():
    """Homepage with recent linksets"""
    recent_linksets = storage.get_recent_linksets(limit=10)
    return render_template('index.html', recent_linksets=recent_linksets)

@app.route('/create', methods=['GET', 'POST'])
def create_linkset():
    """Create a new linkset"""
    form = CreateLinksetForm()
    
    if form.validate_on_submit():
        folder_name = form.folder_name.data.strip()
        links_text = form.links.data.strip()
        password = form.password.data.strip() if form.password.data else None
        expiry_hours = form.expiry_hours.data if form.expiry_hours.data else None
        
        # Parse and validate links
        links = [link.strip() for link in links_text.split('\n') if link.strip()]
        if not links:
            flash('Please provide at least one download link.', 'error')
            return render_template('create.html', form=form)
        
        # Validate URLs
        invalid_urls = validate_urls(links)
        if invalid_urls:
            flash(f'Invalid URLs detected: {", ".join(invalid_urls)}', 'error')
            return render_template('create.html', form=form)
        
        # Generate unique slug
        base_slug = generate_slug(folder_name)
        slug = storage.get_unique_slug(base_slug)
        
        # Calculate expiry
        expires_at = None
        if expiry_hours:
            expires_at = datetime.now() + timedelta(hours=expiry_hours)
        
        # Create linkset
        linkset_id = storage.create_linkset(
            folder_name=folder_name,
            slug=slug,
            links=links,
            password=password,
            expires_at=expires_at
        )
        
        if linkset_id:
            flash('Linkset created successfully!', 'success')
            return redirect(url_for('success', slug=slug))
        else:
            flash('Error creating linkset. Please try again.', 'error')
    
    return render_template('create.html', form=form)

@app.route('/success/<slug>')
def success(slug):
    """Show success page with generated link"""
    linkset = storage.get_linkset_by_slug(slug)
    if not linkset:
        flash('Linkset not found.', 'error')
        return redirect(url_for('index'))
    
    return render_template('success.html', linkset=linkset)

@app.route('/fc/<slug>')
def verify_linkset(slug):
    """Show CAPTCHA verification page"""
    linkset = storage.get_linkset_by_slug(slug)
    if not linkset:
        flash('Linkset not found or may have expired.', 'error')
        return redirect(url_for('index'))
    
    # Check if linkset has expired
    if linkset['expires_at'] and datetime.fromisoformat(linkset['expires_at']) < datetime.now():
        flash('This linkset has expired.', 'error')
        return redirect(url_for('index'))
    
    form = CaptchaForm()
    return render_template('verify.html', form=form, linkset=linkset, 
                         recaptcha_site_key=RECAPTCHA_SITE_KEY)

@app.route('/fc/<slug>/verify', methods=['POST'])
def verify_captcha(slug):
    """Verify CAPTCHA and show links"""
    linkset = storage.get_linkset_by_slug(slug)
    if not linkset:
        flash('Linkset not found or may have expired.', 'error')
        return redirect(url_for('index'))
    
    # Check if linkset has expired
    if linkset['expires_at'] and datetime.fromisoformat(linkset['expires_at']) < datetime.now():
        flash('This linkset has expired.', 'error')
        return redirect(url_for('index'))
    
    form = CaptchaForm()
    
    # Verify reCAPTCHA
    recaptcha_response = request.form.get('g-recaptcha-response')
    if not recaptcha_response or not verify_recaptcha(recaptcha_response):
        flash('Please complete the CAPTCHA verification.', 'error')
        return render_template('verify.html', form=form, linkset=linkset, 
                             recaptcha_site_key=RECAPTCHA_SITE_KEY)
    
    # Check password if required
    if linkset.get('password'):
        entered_password = form.password.data
        if not entered_password or entered_password != linkset['password']:
            flash('Incorrect password.', 'error')
            return render_template('verify.html', form=form, linkset=linkset, 
                                 recaptcha_site_key=RECAPTCHA_SITE_KEY)
    
    # Increment view count
    storage.increment_views(slug)
    
    # Store verification in session to prevent direct access
    session[f'verified_{slug}'] = True
    
    return redirect(url_for('show_links', slug=slug))

@app.route('/fc/<slug>/links')
def show_links(slug):
    """Show download links after verification"""
    # Check if user has been verified
    if not session.get(f'verified_{slug}'):
        return redirect(url_for('verify_linkset', slug=slug))
    
    linkset = storage.get_linkset_by_slug(slug)
    if not linkset:
        flash('Linkset not found or may have expired.', 'error')
        return redirect(url_for('index'))
    
    # Check if linkset has expired
    if linkset['expires_at'] and datetime.fromisoformat(linkset['expires_at']) < datetime.now():
        flash('This linkset has expired.', 'error')
        return redirect(url_for('index'))
    
    # Clear verification session
    session.pop(f'verified_{slug}', None)
    
    return render_template('links.html', linkset=linkset)

@app.route('/api/stats/<slug>')
def get_stats(slug):
    """Get linkset statistics"""
    linkset = storage.get_linkset_by_slug(slug)
    if not linkset:
        return jsonify({'error': 'Linkset not found'}), 404
    
    return jsonify({
        'views': linkset['views'],
        'created_at': linkset['created_at'],
        'expires_at': linkset['expires_at']
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
