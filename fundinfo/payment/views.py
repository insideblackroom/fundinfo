from django.shortcuts import render
from django.views.generic import View
from fundinfo.zarinpalgateway.zarinpal import Zarinpal
from fundinfo.zarinpalgateway.exceptions import ZarinpalException
from fundinfo.core.cart import Cart
from django.conf import settings
from .models import Payment

class VerifyView(View):
    def get(self, request):
        cart = Cart(request)
        zarinpal = Zarinpal(**settings.GATEWAY_CONFIG)
        try:
            status, authority = zarinpal.verify_from_gateway(request)

            if status != "VERIFIED":
                return render(request, "invoices/checkout/checkout_error.html", {"status": status})
            if status == "VERIFIED":
                try:
                    Payment.objects.get(authority=authority, status=Payment.STATUS.PENDING)
                except Payment.DoesNotExist:
                    return render(request, "invoices/checkout/checkout_error.html", {"status": status})
                cart.clear()
                return render(request, "invoices/checkout/checkout_done.html", {"status": status})
        except ZarinpalException:
            return render(request, "invoices/checkout/checkout_error.html", {"status": status})
