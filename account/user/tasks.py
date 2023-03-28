from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(subject, html_message, from_email, recipient_list):
    send_mail(subject, html_message, from_email, recipient_list)
