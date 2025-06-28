from django.views.generic import View
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from .cart import Cart
from .models import Product

class product_list_view(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, "core/products/list.html", {"products": products})

class CartAddView(View):
    def get(self, request, id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=id)
        cart.add(product)
        return HttpResponseRedirect(reverse('core:product_list'))

class CartRemoveView(View):
    def get(self, request, id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=id)
        cart.remove(product)
        return HttpResponseRedirect(reverse('core:product_list'))

class EmptyCartView(View):
    def get(self, request):
        cart = Cart(request)
        cart.clear()
        return HttpResponseRedirect(reverse('core:product_list'))

class ShowCartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'core/products/cart.html', {'cart': cart})
