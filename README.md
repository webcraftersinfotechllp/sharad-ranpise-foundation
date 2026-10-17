# Home Rights India Social Foundation

A modern Flask-based NGO website for Home Rights India Social Foundation. The site is structured for future growth, with reusable templates, modular routes, and placeholder content that can be replaced as the organization expands.

## Features

- Responsive NGO website built with Flask and Jinja2
- Reusable template inheritance for header, footer, and page layouts
- Multi-page navigation covering key NGO engagement areas
- Donation, contact, and FAQ sections prepared for future integrations
- Professional Indian NGO visual style with warm, trustworthy design
- Structured for future admin, CMS, payment gateway, and database modules

## Folder Structure

```text
home-rights-india/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── responsive.css
│   ├── js/
│   │   └── main.js
│   ├── images/
│   └── uploads/
├── templates/
│   ├── base.html
│   ├── header.html
│   ├── footer.html
│   ├── navbar.html
│   ├── index.html
│   ├── about.html
│   ├── programs.html
│   ├── donate.html
│   ├── gallery.html
│   ├── contact.html
│   ├── faq.html
│   ├── 404.html
│   ├── 500.html
│   └── legal/
│       ├── privacy-policy.html
│       ├── terms.html
│       ├── donation-policy.html
│       └── refund-policy.html
└── routes/
    ├── __init__.py
    └── main.py
```

## Installation

### Windows

```powershell
mkdir home-rights-india
cd home-rights-india
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Mac/Linux

```bash
mkdir home-rights-india
cd home-rights-india
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000/
```

## How to Add a New Page

1. Add a new route in `routes/main.py`.
2. Create a matching template in `templates/`.
3. Extend `base.html` and insert page content inside the `content` block.
4. Keep URLs consistent with `url_for()` usage for navigation.

Example:

```python
@main_bp.route("/new-page")
def new_page():
    return render_template("new-page.html")
```

## How to Change the Logo

- Replace the existing logo asset in the relevant image folder.
- Update the HTML in `templates/navbar.html` and `templates/footer.html` to point to the new file.
- Keep file names in the `static/images` folder organized by category.

## How to Change Colours

Edit the CSS variables in `static/css/style.css`:

```css
:root {
  --primary: #1f5d50;
  --secondary: #d99a2b;
  --dark: #17342e;
  --light: #f8f6f0;
  --white: #ffffff;
  --text: #333333;
}
```

## How to Add Images

Place the image in `static/images/` and reference it in templates using:

```html
<img
  src="{{ url_for('static', filename='images/hero/hero-1.jpg') }}"
  alt="Community outreach programme"
/>
```

## How to Change Contact Information

Update the phone number, email address, and address in:

- `templates/header.html`
- `templates/footer.html`
- `templates/contact.html`

## How to Integrate a Payment Gateway Later

The donation code is prepared as a structural placeholder for future integration. Replace the form action and connect your chosen gateway such as Razorpay or Cashfree, while keeping the existing donation form structure and validation logic intact.

## Deployment

This project can be deployed on common Python hosting providers such as:

- Render
- Railway
- PythonAnywhere
- DigitalOcean App Platform
- VPS or dedicated hosting

Before production deployment:

- Set a strong `SECRET_KEY` in the environment
- Add proper environment variables for configuration
- Configure a production-grade web server
- Review legal pages with counsel before public release

## Notes

- This is an initial NGO website foundation and is intentionally structured for easy expansion.
- The project is designed to support future features such as admin panels, databases, volunteer forms, donor dashboards, and CMS modules.
