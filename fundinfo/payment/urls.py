from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("verify/", views.VerifyView.as_view(), name="verify"),
]