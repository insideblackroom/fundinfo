from .models import BaseUser

def exist_user(*, email: str):
    return BaseUser.objects.filter(email__iexact=email).exists()

def exist_user_id(*, id: str):
    try:
        user = BaseUser.objects.get(id=id)
    except BaseUser.DoesNotExist:
        return None
    return user