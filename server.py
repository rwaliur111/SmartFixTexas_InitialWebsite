from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Zoho Configuration - USE APP PASSWORD, NOT REGULAR PASSWORD
ZOHO_EMAIL = os.getenv('ZOHO_EMAIL', 'your_email@zoho.com')
ZOHO_APP_PASSWORD = os.getenv('ZOHO_APP_PASSWORD', 'your_app_password_here')  # ← App password, not regular password
ZOHO_SMTP_SERVER = "smtp.zoho.com"
ZOHO_SMTP_PORT = 587

def send_email(name, email, phone, service, message):
    try:
        # Create email message
        msg = MimeMultipart()
        msg['From'] = ZOHO_EMAIL
        msg['To'] = ZOHO_EMAIL  # Send to yourself
        msg['Subject'] = f"SmartFixTexas Contact: {service} Service Request"
        
        # Email body
        body = f"""
        New contact form submission from SmartFixTexas website:
        
        Name: {name}
        Email: {email}
        Phone: {phone or 'Not provided'}
        Service Needed: {service or 'Not specified'}
        
        Message:
        {message}
        
        ---
        Sent from SmartFixTexas website contact form
        """
        
        msg.attach(MimeText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(ZOHO_SMTP_SERVER, ZOHO_SMTP_PORT)
        server.starttls()
        server.login(ZOHO_EMAIL, ZOHO_APP_PASSWORD)  # Use app password here
        server.sendmail(ZOHO_EMAIL, ZOHO_EMAIL, msg.as_string())
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Email error: {str(e)}")
        return False

@app.route('/api/send-email', methods=['POST'])
def handle_contact_form():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({
                'success': False,
                'message': 'Please fill in all required fields (name, email, message).'
            }), 400
        
        # Send email
        email_sent = send_email(
            data.get('name', ''),
            data.get('email', ''),
            data.get('phone', ''),
            data.get('service', ''),
            data.get('message', '')
        )
        
        if email_sent:
            return jsonify({
                'success': True,
                'message': 'Thank you for your message! We will contact you shortly.'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Sorry, there was an error sending your message. Please call us directly at (512) 481-2587.'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An internal server error occurred. Please try again later.'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)