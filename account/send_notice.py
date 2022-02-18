from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import OTP
from fitila import settings
from rest_framework import serializers
from django.template.loader import render_to_string

User = get_user_model()

def send_notification(user:User, status, reason=""):
    if status=='pending':
        
        subject = "YOUR BUSINESS IS PENDING"
        
        message = f"""Hello, {user.first_name}.\nThank you for listing your business on the Enterprise Data Map. Your entry is currently pending approval from our administrative team. You will be notified as soon as your entry has been approved
Cheers,
Enterprise Data Map Team                
"""   
        msg_html = render_to_string('notification/pending.html', {
                        'first_name': str(user.first_name).title(),
                        })
        
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail( subject, message, email_from, recipient_list, html_message=msg_html)
        
    elif status=='approved':
        subject = "YOUR BUSINESS HAS BEEN APPROVED"
        
        message = f"""Hello, {user.first_name}.\nYou business has been approved and is now available on the Enterprise Data Map.
Cheers,
Enterprise Data Map Team               
"""   
        msg_html = render_to_string('notification/approved.html', {
                        'first_name': str(user.first_name).title(),
                        })
        
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail( subject, message, email_from, recipient_list, html_message=msg_html)
        
        
    elif status=='rejected':
        subject = "UPDATE ON YOUR BUSINESS"
        
        message = f"""Hello, {user.first_name}.\nThank you for listing your business on the Enterprise Data Map Platform.Unfortunately, your entry cannot be approved by this time. The reason(s) for entry rejection is listed below:\n{reason}\nYou can always login into your profile to make any necessary changes.

Cheers,
Enterprise Data Map Team
                
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
        
