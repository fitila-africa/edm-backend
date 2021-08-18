from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    token = "https://www.edm.com/forgot-password/{}".format(reset_password_token.key)
    
    send_mail(
        subject = "Password Reset for OyoyoNG",

        message= 'Hello {},\n\nYou are receiving this message because you or someone else have requested the reset of the password for your account.\nPlease click on the following link, or paste this into your browser to complete the process within 24hours of receiving it:\n{}\n\nPlease if you did not request this please ignore this e-mail and your password would remain unchanged.\n\nRegards,\nOyoyoNG Support'.format(reset_password_token.user.first_name, token),
        
        from_email  = 'admin@edm.com',
        recipient_list= [reset_password_token.user.email]
    )