from django.shortcuts import render
from django.views.generic import View
from fundinfo.zarinpalgateway.zarinpal import Zarinpal
from fundinfo.zarinpalgateway.exceptions import ZarinpalException
from fundinfo.core.cart import Cart
from django.conf import settings

class VerifyView(View):
    def get(self, request):
        cart = Cart(request)
        zarinpal = Zarinpal(**settings.GATEWAY_CONFIG)
        try:
            status = zarinpal.verify_from_gateway(request)
            print(status)
            if status != "VERIFIED":
                return render(request, "invoices/checkout/checkout_error.html", {"status": status})
            cart.clear()
        except ZarinpalException:
            return render(request, "invoices/checkout/checkout_error.html", {"status": status})
        return render(request, "invoices/checkout/checkout_done.html", {"status": status})
