from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings



@shared_task
def send_welcome_email(username, user_email):

    subject = f" Hello {username}. Welcome to Servify."
    message = f"Hi {username}, Thankyou for connecting with Servify."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

