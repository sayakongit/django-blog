from django.core.mail import send_mail
from django.conf import settings

URL = 'https://web-production-d9c5.up.railway.app'


def send_forget_password_mail(email, token):
    subject = '[Action Required] News & Blogs | Password Reset Mail'
    message = f'Hi , click on the link to reset your password {URL}/change_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
