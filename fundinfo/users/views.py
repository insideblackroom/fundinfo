from django.views.generic import View
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from fundinfo.emails.services import email_send
from fundinfo.emails.models import Email
from fundinfo.emails.services import email_create
from fundinfo.common.services import model_update
from .selectors import exist_user_id
from . import forms

token_generator = PasswordResetTokenGenerator()

def link_generator(request, user):
    base_url = "http://{0}/{1}"
    domain = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(str(user.pk)))
    token = token_generator.make_token(user)
    url = reverse('activate', kwargs={"uid": uid, "token": token})
    return base_url.format(domain, url)

class SignUpView(View):
    def get(self, request):
        form = forms.SignUpForm()
        return render(request, "users/signup.html", {"form": form})

    def post(self, request):
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            subject = 'Please activate your account'
            to = user.email
            html = render_to_string('users/signup_email.html', {'link': link_generator(request, user)})
            email = email_create(subject=subject, to=to, html=html, status=Email.Status.READY)
            email_send(email)
            return render(request, "users/signup_done.html", {"email": to})
        return render(request, "users/signup.html", {'form': form})

class SignUpActivateView(View):
    def get(self, request, uid, token):
        id = force_str(urlsafe_base64_decode(uid))
        user = exist_user_id(id=id)
        if not user or user.is_active:
            return render(request, 'users/activate_error.html')
        if token_generator.check_token(user, token):
            user, _ = model_update(instance=user, fields=['is_active'], data={"is_active": True})
            return render(request, 'users/activate_done.html')
        return render(request, 'users/activate_error.html')
        
