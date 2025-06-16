# MileCrypt - Secure Link Locker

A Flask-based public link locker application with CAPTCHA protection, similar to FileCrypt.cc. Users can create protected link sets without registration, and access is controlled through Google reCAPTCHA verification.

## Features

- **Public Link Creation**: No registration required - anyone can create protected link sets
- **CAPTCHA Protection**: Google reCAPTCHA verification before accessing download links  
- **Organized Link Sets**: Group multiple download URLs under custom folder names
- **Optional Security**: Password protection and automatic expiry times
- **Modern UI**: Responsive Bootstrap design with dark/light theme toggle
- **SQLite Storage**: Simple file-based database (in-memory for demo)
- **Mobile Friendly**: Fully responsive design works on all devices

## How It Works

1. **Create**: Enter a folder name and multiple download URLs
2. **Generate**: Get a unique protected link (e.g., `/fc/your-folder-name`)
3. **Share**: Share the protected link with others
4. **Verify**: Users complete CAPTCHA (and password if set) to access links
5. **Download**: All download links are revealed after verification

## Installation

### Local Development

1. Clone the repository
2. Install Python 3.11+ 
3. Install dependencies:
   ```bash
   pip install -r requirements_deploy.txt
   ```
4. Set environment variables:
   ```bash
   export SESSION_SECRET="your-secret-key"
   export RECAPTCHA_SITE_KEY="your-recaptcha-site-key"
   export RECAPTCHA_SECRET_KEY="your-recaptcha-secret-key"
   ```
5. Run the application:
   ```bash
   python main.py
   ```

### Deploy to Render

1. Push code to GitHub
2. Connect repository to Render
3. Use the included `render.yaml` for automatic configuration
4. Set your reCAPTCHA keys in environment variables

### Deploy to Heroku

1. Push code to GitHub
2. Create new Heroku app
3. Use the included `Procfile` for configuration
4. Set environment variables in Heroku settings

## Environment Variables

- `SESSION_SECRET`: Flask session secret key (required)
- `RECAPTCHA_SITE_KEY`: Google reCAPTCHA site key (optional, uses test key by default)
- `RECAPTCHA_SECRET_KEY`: Google reCAPTCHA secret key (optional, uses test key by default)

## File Structure

```
milecrypt/
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── models.py             # Data storage models
├── forms.py              # WTForms form classes
├── utils.py              # Utility functions
├── templates/            # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── create.html
│   ├── success.html
│   ├── verify.html
│   └── links.html
├── static/               # Static assets
│   ├── css/style.css
│   └── js/app.js
├── render.yaml           # Render deployment config
├── Procfile              # Heroku deployment config
└── requirements_deploy.txt # Python dependencies
```

## Security Features

- **CAPTCHA Protection**: Prevents automated bot access
- **Password Protection**: Optional additional security layer
- **Link Expiry**: Automatic expiration for sensitive content
- **URL Validation**: All submitted URLs are validated
- **Session Management**: Secure session handling
- **Input Sanitization**: All user inputs are properly sanitized

## Usage Examples

### Creating a Link Set

1. Visit the homepage
2. Click "Create Protected Links"
3. Enter folder name: "My Software Package"
4. Add download URLs (one per line):
   ```
   https://example.com/file1.zip
   https://example.com/file2.exe
   https://example.com/file3.pdf
   ```
5. Set optional password and expiry
6. Click "Create Protected Links"
7. Copy the generated protected link

### Accessing Protected Links

1. Visit the protected link (e.g., `/fc/my-software-package`)
2. Complete the CAPTCHA verification
3. Enter password if required
4. View and download all files

## Customization

### Changing Theme Colors

Edit `static/css/style.css` and modify the CSS variables:

```css
:root {
    --bs-primary: #your-color;
    --bs-success: #your-color;
}
```

### Adding Languages

The application is ready for internationalization. Add translation files and modify templates as needed.

### Custom CAPTCHA

Replace Google reCAPTCHA with custom solutions by modifying the verification logic in `app.py`.

## API Endpoints

- `GET /` - Homepage with recent link sets
- `GET /create` - Create new link set form
- `POST /create` - Process link set creation
- `GET /success/<slug>` - Show success page with generated link
- `GET /fc/<slug>` - CAPTCHA verification page
- `POST /fc/<slug>/verify` - Process CAPTCHA verification
- `GET /fc/<slug>/links` - Show download links after verification
- `GET /api/stats/<slug>` - Get link set statistics (JSON)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue on the repository.

## Changelog

### v1.0.0
- Initial release
- Public link creation without registration
- Google reCAPTCHA integration
- Password protection and expiry options
- Responsive Bootstrap UI
- Dark/light theme toggle
- Enhanced copy functionality with toast notifications