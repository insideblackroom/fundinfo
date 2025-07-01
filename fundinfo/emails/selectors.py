from .models import Email

def email_get_id(*, email_id):
    email = Email.objects.get(id=email_id)
    return email
