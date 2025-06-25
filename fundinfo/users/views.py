from django.views.generic import View
from django.shortcuts import render
from . import forms

class SignUpView(View):
    def get(self, request):
        form = forms.SignUpForm()
        return render(request, "users/signup.html", {"form": form})

    def post(self, request):
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            return render(request, "users/signup_done.html", {"user_email": cd['email']})
        return render(request, "users/signup.html", {'form': form})