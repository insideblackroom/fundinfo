from .models import BaseUser

def exist_user(*, email: str):
    return BaseUser.objects.filter(email__iexact=email).exists()
