from django.shortcuts import render
from django.views.generic import View
from fundinfo.core.cart import Cart
from .forms import InvoiceForm

class CheckoutView(View):
    def get(self, request):
        cart = Cart(request)
        invoice_form = InvoiceForm()
        return render(
            request,
            'invoices/checkout/checkout.html',
            {'cart': cart, 'form': invoice_form}
        )

    def post(self, request):
        ...