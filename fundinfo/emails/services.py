from django.core.mail import EmailMultiAlternatives
from .models import Email
from django.db import transaction
from config.env import env
from fundinfo.common.services import model_update
from django.utils import timezone
from .models import Email

@transaction.atomic()
def email_create(*, subject, to, html, status, plain_text=None):
    email = Email.objects.create(subject=subject, plain_text=plain_text, to=to, html=html, status=status)
    email.full_clean()
    email.save()
    return email

@transaction.atomic()
def email_send(email: Email):
    subject = email.subject
    to = email.to
    html = email.html
    plain_text = email.plain_text
    from_email = env("MAILTRAP_EMAIL_HOST_USER")
    mail = EmailMultiAlternatives(subject, plain_text, from_email, [to])
    mail.attach_alternative(html, "text/html")
    
    if mail.send(): 
        update_email, _ = model_update(
            instance=email,
            fields=['sent_at', 'status'],
            data={'sent_at': timezone.now(), 'status': Email.Status.SENT}
        )
        return update_email
    return email