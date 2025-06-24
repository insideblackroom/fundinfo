from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.utils.html import format_html
from phonenumber_field.formfields import PhoneNumberField
from .models import BaseUser
from .selectors import exist_user

class SignUpForm(forms.Form):

    error_message = {
        "password_mismatch": "The Password Fields did not match"
    }

    email = forms.EmailField(
        label="Your Email Address",
        widget=forms.EmailInput(attrs={"placeholder": "E-mail Address"})
    )

    password = forms.CharField(
        label="New Password",
        max_length=255,
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    confirm_password = forms.CharField(
        label="New Confirm Password",
        max_length=255,
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        help_text=format_html("<ul><li>{}</li></ul>", "Password Confirmation"),
    )

    # phone = forms.CharField(max_length=255, 
    #                         validators=[
    #                         validators.RegexValidator(r"(\+98|09|9)?9\d(8)$"),
    #                         validators.MinLengthValidator(5),
    #                         validators.MaxLengthValidator(20)
    #                         ])
    phone = PhoneNumberField()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and exist_user(email=email):
            raise ValidationError(
                "email exist"
            )
        elif self.data['email'] == self.data['password']:
            raise ValidationError("name and password must not same")
        else:
            return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_message['password_mismatch'],
                    code="password_mismatch"
                )
        password_validation.validate_password(password2)
        return cleaned_data

    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        pass