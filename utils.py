import re
from urllib.parse import urlparse

def generate_slug(folder_name):
    """Generate a URL-safe slug from folder name"""
    # Convert to lowercase and replace spaces with hyphens
    slug = folder_name.lower().strip()
    # Remove special characters except hyphens and alphanumeric
    slug = re.sub(r'[^\w\s-]', '', slug)
    # Replace spaces and multiple hyphens with single hyphen
    slug = re.sub(r'[\s_-]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    # Limit length
    slug = slug[:50]
    
    return slug or 'linkset'

def validate_urls(urls):
    """Validate a list of URLs and return invalid ones"""
    invalid_urls = []
    
    for url in urls:
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                invalid_urls.append(url)
            elif result.scheme not in ['http', 'https']:
                invalid_urls.append(url)
        except Exception:
            invalid_urls.append(url)
    
    return invalid_urls

def format_datetime(dt_string):
    """Format datetime string for display"""
    if not dt_string:
        return None
    
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return dt_string
