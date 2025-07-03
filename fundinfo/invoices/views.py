from django.shortcuts import render
from django.views.generic import View
from fundinfo.core.cart import Cart
from .forms import InvoiceForm
from .models import InvoiceItem
from fundinfo.payment.models import Payment
from .utils import get_user_ip
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from decimal import Decimal
import requests as rq
from fundinfo.zarinpalgateway.zarinpal import Zarinpal
from django.conf import settings

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
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            cart = Cart(request)
            invoice.total = cart.get_total_price()
            invoice.save()

            invoice_item_objs = []
            for item in cart:
                product = item.get('product')
                invoice_item = InvoiceItem()
                invoice_item.invoice = invoice
                invoice_item.product = product
                invoice_item.name = product.name
                invoice_item.count = item.get('quantity')
                invoice_item.price = product.price
                invoice_item.discount = product.discount
                invoice_item.total = item.get('total_price') - (item.get('total_price') * Decimal(invoice_item.discount))
                invoice_item_objs.append(invoice_item)
            InvoiceItem.objects.bulk_create(invoice_item_objs)

            payment = Payment()
            payment.invoice = invoice
            payment.total = invoice.total - (invoice.total * invoice.discount)
            payment.total += payment.total * Decimal(invoice.vat)
            payment.descrption = "خرید از سایت"
            payment.user_ip = get_user_ip(request)

            zarinpal = Zarinpal(**settings.GATEWAY_CONFIG)
            zarinpal.set_amount(payment.total)
            callback_url = "http://"+str(get_current_site(request))+reverse("payment:verify")
            zarinpal.set_callback_url(callback_url)
    
            gateway = zarinpal.init_gateway()
            payment.authority = gateway.ref_id
            payment.save() 
            return zarinpal.redirect_gateway()
        return render(request, 'invoices/checkout/checkout.html', {'form': form})
