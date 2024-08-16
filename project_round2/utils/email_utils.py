import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app

def send_email(to_email, subject, content):
    message = Mail(
        from_email=current_app.config['DEFAULT_FROM_EMAIL'],
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    try:
        sg = SendGridAPIClient(current_app.config['SENDGRID_API_KEY'])
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(str(e))
        return None

def send_invite_email(to_email, invite_link):
    subject = "You're Invited to Join Our Organization"
    content = f"<p>Please click the link below to join:</p><a href='{invite_link}'>Join Now</a>"
    return send_email(to_email, subject, content)

def send_password_update_alert(to_email):
    subject = "Password Updated Successfully"
    content = "<p>Your password has been updated successfully. If this wasn't you, please contact support immediately.</p>"
    return send_email(to_email, subject, content)

def send_login_alert(to_email):
    subject = "New Login Detected"
    content = "<p>A new login to your account was detected. If this wasn't you, please contact support immediately.</p>"
    return send_email(to_email, subject, content)
