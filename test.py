# Quick test script
import smtplib

try:
    server = smtplib.SMTP("smtp.zoho.com", 587)
    server.starttls()
    server.login("your_email@zoho.com", "your_regular_password")  # This will likely fail
    print("Regular password works (unlikely)")
except Exception as e:
    print(f"Regular password failed: {e}")
    print("You need to use an App Password")