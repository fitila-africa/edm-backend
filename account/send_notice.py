from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import OTP
from fitila import settings
from rest_framework import serializers
from django.template.loader import render_to_string


def send_notification(user, status, reason=""):
    if status=='pending':
        
        subject = "YOUR BUSINESS IS PENDING"
        
        message = f"""Hello, {user.first_name}.\nThank you for listing your business on the enterprise data map platform. You entry is pending approval from our administrative team and you would be notified as soon as that is done.
Cheers,
EDM Admin                
"""   
        msg_html = render_to_string('notification/pending.html', {
                        'first_name': str(user.first_name).title(),
                        })
        
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail( subject, message, email_from, recipient_list, html_message=msg_html)
        
    elif status=='approved':
        subject = "YOUR BUSINESS HAS BEEN APPROVED"
        
        message = f"""Hello, {user.first_name}.\nYou entry has been approved and is now available on the EDM platform.
Cheers,
EDM Admin                
"""   
        msg_html = render_to_string('notification/approved.html', {
                        'first_name': str(user.first_name).title(),
                        })
        
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail( subject, message, email_from, recipient_list, html_message=msg_html)
        
        
    elif status=='rejected':
        subject = "UPDATE ON YOUR BUSINESS"
        
        message = f"""Hello, {user.first_name}.\nThank you for listing your business on the enterprise data map platform. Unfortunately, your entry cannot be approved at this time.\Here is the reason for the rejection at this time:\n{reason}\nYou can always login to your portal and make the necessary changes.
Cheers,
EDM Admin                
"""   
        msg_html = render_to_string('notification/rejected.html', {
                        'first_name': str(user.first_name).title(),
                        'reason' : reason
                        })
        
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail( subject, message, email_from, recipient_list, html_message=msg_html)
        
    elif status=='updated':
        subject = "YOUR BUSINESS HAS JUST BEEN UPDATED"
        
        message = f"""Hello, {user.first_name}.\nWe  noticed an update your entry. This update is pending approval from our administrative team and you would be notified as soon as that is done.
Cheers,
EDM Admin                
"""   
        msg_html = render_to_string('notification/update.html', {
                        'first_name': str(user.first_name).title(),
        
                        })
        
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail( subject, message, email_from, recipient_list, html_message=msg_html)
        
