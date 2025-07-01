from celery import shared_task
from fundinfo.emails.selectors import email_get_id
from fundinfo.emails.services import email_send

@shared_task
def user_signup_email_send(email_id):
    email = email_get_id(email_id=email_id)
    email_sent = email_send(email)
    return email