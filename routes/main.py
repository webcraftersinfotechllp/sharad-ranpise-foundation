import smtplib
import threading
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fpdf import FPDF
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
import razorpay

from models import ContactMessage, Donation, db
from datetime import datetime
import os
from dotenv import load_dotenv

# .env फाईल मधील माहिती वाचण्यासाठी
load_dotenv()

# .env मधून माहिती घ्या
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

main_bp = Blueprint("main", __name__)


def generate_receipt_pdf(donor_name, amount, pan_number, payment_id):
  pdf = FPDF()
  pdf.add_page()
  pdf.set_font("Helvetica", "B", 18)
  pdf.cell(0, 12, "SHARAD RANPISE FOUNDATION", ln=True)
  pdf.set_font("Helvetica", "", 12)
  pdf.cell(0, 10, "Donation Receipt & Acknowledgement", ln=True)
  pdf.ln(10)
  current_date = datetime.now().strftime("%d-%m-%Y")
  pdf.cell(0, 10, "Donation Receipt Status: Success", ln=True)
  pdf.cell(0, 10, f"Donor Name: {donor_name}", ln=True)
  pdf.cell(0, 10, f"Payment ID: {payment_id}", ln=True)
  pdf.cell(0, 10, f"Amount: Rs. {amount:.2f}", ln=True)
  pdf.cell(0, 10, f"PAN Number: {pan_number if pan_number else 'N/A'}", ln=True)
  pdf.cell(0, 10, f"Date: {current_date}", ln=True)  # <--- ही ओळ नवीन ॲड केली आहे
  pdf.ln(12)
  pdf.multi_cell(
      0,
      10,
      "This document serves as a formal acknowledgement of your donation. Thank you for supporting our mission.",
  )
  return pdf.output(dest="S")


def send_receipt_email(
    donor_email, donor_name, amount, pan_number, payment_id
):
  """Sends donation receipt email via SMTP with a downloadable PDF attachment."""
  try:
    current_date = datetime.now().strftime("%d-%m-%Y")
    msg = MIMEMultipart("alternative")
    msg["From"] = f"SHARAD RANPISE FOUNDATION <{SENDER_EMAIL}>"
    msg["To"] = donor_email
    msg["Subject"] = (
        "Donation Receipt & Acknowledgement - SHARAD RANPISE"
        " FOUNDATION"
    )

    html_body = f"""
    <html>
      <body style="margin:0; padding:0; background-color:#f4f7f6; font-family:Arial, sans-serif; color:#1a1a1a;">
        <div style="max-width:680px; margin:30px auto; background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; overflow:hidden;">
          <div style="background:linear-gradient(135deg, #1d4d3c, #2d6a52); padding:28px 32px; color:#ffffff;">
            <h2 style="margin:0; font-size:26px; font-weight:bold;">SHARAD RANPISE FOUNDATION</h2>
            <p style="margin:10px 0 0; font-size:14px; letter-spacing:0.4px; opacity:0.9;">Donation Receipt & Acknowledgement</p>
          </div>

          <div style="padding:28px 32px 20px;">
            <p style="margin:0 0 18px; font-size:15px; line-height:1.6; color:#2f2f2f;">
              Dear <strong>{donor_name}</strong>,<br><br>
              Thank you for your generous contribution of <strong>Rs. {amount:.2f}</strong> to SHARAD RANPISE FOUNDATION.
            </p>

            <div style="margin:20px 0 26px; padding:12px 16px; background:#ecfdf5; border:1px solid #a7f3d0; border-radius:8px; color:#065f46; font-weight:bold; display:inline-block;">
              ✓ Payment Success
            </div>

            <table style="width:100%; border-collapse:collapse; background:#f9fafb; border:1px solid #e5e7eb; border-radius:10px; overflow:hidden;">
              <tr style="background:#ffffff; border-bottom:1px solid #e5e7eb;">
                <td style="padding:14px 16px; font-weight:bold; width:40%; color:#374151;">Payment ID</td>
                <td style="padding:14px 16px; color:#111827;">{payment_id}</td>
              </tr>
              <tr style="background:#ffffff; border-bottom:1px solid #e5e7eb;">
                <td style="padding:14px 16px; font-weight:bold; color:#374151;">Donor Name</td>
                <td style="padding:14px 16px; color:#111827;">{donor_name}</td>
              </tr>
              <tr style="background:#ffffff; border-bottom:1px solid #e5e7eb;">
                <td style="padding:14px 16px; font-weight:bold; color:#374151;">Amount</td>
                <td style="padding:14px 16px; color:#111827;">Rs. {amount:.2f}</td>
              </tr>
              <tr style="background:#ffffff;">
                <td style="padding:14px 16px; font-weight:bold; color:#374151;">PAN Number</td>
                <td style="padding:14px 16px; color:#111827;">{pan_number if pan_number else 'N/A'}</td>
              </tr>
              <tr style="background:#ffffff; border-bottom:1px solid #e5e7eb;">
                <td style="padding:14px 16px; font-weight:bold; color:#374151;">Date</td>
                <td style="padding:14px 16px; color:#111827;">{current_date}</td>
              </tr>
            </table>

            <p style="margin:24px 0 0; font-size:14px; line-height:1.7; color:#374151;">
              This email serves as an official confirmation of your donation. Your Section 80G tax benefit documentation is recorded under your registered PAN.
            </p>

            <p style="margin:22px 0 0; font-size:14px; color:#374151;">
              Regards,<br>
              <strong>SHARAD RANPISE FOUNDATION</strong><br>
              Email: info@sharadranpisefoundation.in
            </p>
          </div>
        </div>
      </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html", "utf-8"))

    pdf_bytes = generate_receipt_pdf(
        donor_name=donor_name,
        amount=amount,
        pan_number=pan_number,
        payment_id=payment_id,
    )
    attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
    attachment.add_header(
        "Content-Disposition",
        "attachment",
        filename=f"Donation_Receipt_{payment_id}.pdf",
    )
    msg.attach(attachment)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, donor_email, msg.as_string())
    server.quit()
    return True
  except Exception as e:
    print("SMTP Mail Error:", e)
    return False


def send_contact_notification(name, email, phone, subject, message):
  """Sends a new contact inquiry email to the site admin via SMTP."""
  try:
    msg = MIMEMultipart()
    msg["From"] = f"Website Inquiry <{SENDER_EMAIL}>"
    msg["To"] = SENDER_EMAIL
    msg["Subject"] = f"New Contact Inquiry: {subject}"

    body = f"""Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject}

Message:
{message}
"""
    msg.attach(MIMEText(body, "plain", "utf-8"))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, SENDER_EMAIL, msg.as_string())
    server.quit()
    return True
  except Exception as e:
    print("SMTP Contact Notification Error:", e)
    return False


# ==========================================
# Data Structures (Programs, Projects, etc.)
# ==========================================

impact_stats = [
    {"label": "Communities Reached", "value": 48, "suffix": "+"},
    {"label": "People Supported", "value": 24000, "suffix": "+"},
    {"label": "Programs Conducted", "value": 120, "suffix": "+"},
    {"label": "Volunteers & Supporters", "value": 850, "suffix": "+"},
]

get_involved_cards = [
    {
        "title": "Donate",
        "description": (
            "Support families, learners, and communities with direct,"
            " impact-led contributions."
        ),
        "link": "/donate",
    },
    {
        "title": "Volunteer",
        "description": (
            "Share your time, skills, and energy to strengthen local action."
        ),
        "link": "/contact",
    },
    {
        "title": "Partner With Us",
        "description": (
            "Collaborate with a mission-led team building lasting community"
            " outcomes."
        ),
        "link": "/contact",
    },
    {
        "title": "CSR Collaboration",
        "description": (
            "Create measurable social impact through aligned corporate"
            " partnerships."
        ),
        "link": "/contact",
    },
]

faqs = [
    {
        "question": "What does the foundation do?",
        "answer": (
            "Home Rights India Social Foundation works across education,"
            " health, livelihoods, women and youth empowerment, rights"
            " awareness, and community development to create equitable"
            " opportunities for underserved communities."
        ),
    },
    {
        "question": "How can I donate?",
        "answer": (
            "You can donate through our donation page, where you can choose a"
            " one-time amount or a custom contribution. We also provide banking"
            " and UPI details for future integration with secure payment"
            " systems."
        ),
    },
    {
        "question": "Can I volunteer?",
        "answer": (
            "Yes. We welcome volunteers who can support field outreach,"
            " research, communication, event support, community engagement,"
            " and programme coordination."
        ),
    },
    {
        "question": "Can corporates partner with the foundation?",
        "answer": (
            "Yes. We work with corporate partners to create CSR-aligned"
            " programmes, employee engagement opportunities, and social"
            " initiatives that create measurable community impact."
        ),
    },
    {
        "question": "How can an NGO/community request support?",
        "answer": (
            "You can contact us through our contact form or reach out via email"
            " and phone to share your request, needs, and partnership intent."
        ),
    },
    {
        "question": "How can I collaborate with the foundation?",
        "answer": (
            "You can connect via the contact page or by reaching out to our"
            " team for institutional partnerships, programme collaborations,"
            " or resource support."
        ),
    },
]


# ==========================================
# Routes
# ==========================================
@main_bp.route("/")
def home():
  return render_template(
      "index.html",
      impact_stats=impact_stats,
      get_involved=get_involved_cards,
  )


@main_bp.route("/about")
def about():
  return render_template("about.html")


@main_bp.route("/programs")
def programs_page():
  return render_template("programs.html")


@main_bp.route("/donate", methods=["GET", "POST"])
def donate():
  if request.method == "POST":
    try:
      amount = float(request.form.get("amount", 1000))
      purpose = request.form.get("purpose", "General Support")
      donor_name = request.form.get("name", "").strip()
      mobile = request.form.get("mobile", "").strip()
      email = request.form.get("email", "").strip()
      pan_number = request.form.get("pan", "").strip()

      # 1. Backend Validation
      donor_errors = []
      if amount < 1:
        donor_errors.append("Please enter a valid donation amount.")
      if not donor_name:
        donor_errors.append("Please enter your full name.")
      if not mobile or len(mobile) != 10:
        donor_errors.append("Please enter a valid 10-digit mobile number.")
      if not email or "@" not in email:
        donor_errors.append("Please enter a valid email address.")

      if donor_errors:
        return render_template("donate.html", donor_errors=donor_errors)

      # 2. Razorpay Client initialize करणे
      client = razorpay.Client(
          auth=(
              current_app.config["RAZORPAY_KEY_ID"],
              current_app.config["RAZORPAY_KEY_SECRET"],
          )
      )

      # 3. Order तयार करणे (Amount पैशांमध्ये असते, त्यामुळे x 100)
      order_data = {
          "amount": int(amount * 100),
          "currency": "INR",
          "payment_capture": "1",
      }
      razorpay_order = client.order.create(data=order_data)

      # 4. सुरुवातीची 'Pending' नोंद SQLite मध्ये सेव्ह करणे
      new_donation = Donation(
          donor_name=donor_name,
          mobile=mobile,
          email=email,
          amount=amount,
          purpose=purpose,
          pan_number=pan_number if pan_number else None,
          razorpay_order_id=razorpay_order["id"],
          payment_status="Pending",
      )
      db.session.add(new_donation)
      db.session.commit()

      # 5. Modal पॉप-अपसाठी डेटा फ्रंटएंडला पाठवणे
      return render_template(
          "donate.html",
          checkout_popup=True,
          razorpay_order_id=razorpay_order["id"],
          razorpay_key_id=current_app.config["RAZORPAY_KEY_ID"],
          amount=int(amount * 100),
          donor_name=donor_name,
          email=email,
          mobile=mobile,
      )

    except Exception as e:
      db.session.rollback()
      return render_template(
          "donate.html",
          donor_errors=["Unable to initiate payment. Please try again."],
      )

  return render_template("donate.html")


@main_bp.route("/payment/verify", methods=["POST"])
def payment_verify():
  data = request.get_json()
  razorpay_order_id = data.get("razorpay_order_id")
  razorpay_payment_id = data.get("razorpay_payment_id")
  razorpay_signature = data.get("razorpay_signature")

  client = razorpay.Client(
      auth=(
          current_app.config["RAZORPAY_KEY_ID"],
          current_app.config["RAZORPAY_KEY_SECRET"],
      )
  )

  try:
    # 1. Signature तपासणे (सुरक्षेसाठी)
    client.utility.verify_payment_signature({
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "razorpay_signature": razorpay_signature,
    })

    # 2. DB मधील रेकॉर्ड अपडेट करून Success करणे
    donation = Donation.query.filter_by(
        razorpay_order_id=razorpay_order_id
    ).first()
    if donation:
      donation.razorpay_payment_id = razorpay_payment_id
      donation.razorpay_signature = razorpay_signature
      donation.payment_status = "Success"
      db.session.commit()

      # 3. SweetAlert च्या आधी डोनरच्या ईमेलवर Receipt पाठवणे
      send_receipt_email(
          donor_email=donation.email,
          donor_name=donation.donor_name,
          amount=donation.amount,
          pan_number=donation.pan_number,
          payment_id=razorpay_payment_id,
      )

    return jsonify({"status": "success"})

  except razorpay.errors.SignatureVerificationError:
    donation = Donation.query.filter_by(
        razorpay_order_id=razorpay_order_id
    ).first()
    if donation:
      donation.payment_status = "Failed"
      db.session.commit()
    return (
        jsonify({"status": "failed", "message": "Payment Verification Failed"}),
        400,
    )


@main_bp.route("/gallery")
def gallery():
  gallery_items = [
      {
          "category": "Education",
          "title": "Learning session",
          "image": "images/gallery/img1.avif",
      },
      {
          "category": "Health",
          "title": "Community health awareness",
          "image": "images/gallery/img2.avif",
      },
      {
          "category": "Women Empowerment",
          "title": "Leadership workshop",
          "image": "images/gallery/img3.avif",
      },
      {
          "category": "Community Development",
          "title": "Local mobilization",
          "image": "images/gallery/img4.avif",
      },
  ]
  return render_template("gallery.html", gallery_items=gallery_items)


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
  if request.method == "POST":
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip()
    mobile = (request.form.get("mobile") or "").strip()
    subject = (request.form.get("subject") or "Inquiry").strip()
    message = (request.form.get("message") or "").strip()

    # 1. Backend Validation Check
    contact_errors = []
    if not name or len(name) < 3:
      contact_errors.append(
          "Please enter a valid full name (at least 3 characters)."
      )
    if not email or "@" not in email:
      contact_errors.append("Please enter a valid email address.")
    if not mobile or len(mobile) != 10:
      contact_errors.append("Please enter a valid 10-digit mobile number.")
    if not subject or len(subject) < 5:
      contact_errors.append(
          "Please enter a subject (at least 5 characters)."
      )
    if not message or len(message) < 10:
      contact_errors.append(
          "Please write a message (at least 10 characters)."
      )

    if contact_errors:
      return render_template("contact.html", contact_errors=contact_errors)

    # 2. Database मध्ये डेटा सेव्ह करणे
    try:
      new_message = ContactMessage(
          name=name,
          email=email,
          mobile=mobile,
          subject=subject,
          message=message,
      )
      db.session.add(new_message)
      db.session.commit()

      try:
        threading.Thread(
            target=send_contact_notification,
            args=(name, email, mobile, subject, message),
            daemon=True,
        ).start()
      except Exception:
        pass

      return jsonify({
          "status": "success",
          "success": True,
          "message": "Message sent successfully!",
      }), 200

    except Exception as e:
      print(str(e))
      db.session.rollback()
      return jsonify({
          "status": "error",
          "success": False,
          "message": "Something went wrong while saving your message. Please try again.",
      }), 500

  return render_template("contact.html")


@main_bp.route("/faq")
def faq():
  return render_template("faq.html", faqs=faqs)


@main_bp.route("/privacy-policy")
def privacy_policy():
  return render_template("legal/privacy-policy.html")


@main_bp.route("/terms")
def terms():
  return render_template("legal/terms.html")


@main_bp.route("/donation-policy")
def donation_policy():
  return render_template("legal/donation-policy.html")


@main_bp.route("/refund-policy")
def refund_policy():
  return render_template("legal/refund-policy.html")