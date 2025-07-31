from django.views.generic import View
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from .cart import Cart
from .models import Product
from .forms import CartAddProductForm

class product_list_view(View):
    def get(self, request):
        products = Product.objects.all()
        cart_form = CartAddProductForm()
        return render(request, "core/products/list.html", {"products": products, 'cart_add_product_form': cart_form})

def product_detail(request):
    ...

class CartAddView(View):
    def get(self, request, id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=id)
        form = CartAddProductForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(
                product, cd['quantity'], override=cd['override']
            )
        return HttpResponseRedirect(reverse('core:cart'))

def cart_append(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product)
    return HttpResponseRedirect(reverse('core:cart'))

class CartRemoveView(View):
    def get(self, request, id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=id)
        cart.remove(product)
        return HttpResponseRedirect(reverse('core:cart'))

class EmptyCartView(View):
    def get(self, request):
        cart = Cart(request)
        cart.clear()
        return HttpResponseRedirect(reverse('core:product_list'))

class ShowCartView(View):
    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(
                initial={'quantity': item['quantity'], 'override': True}
            )

        return render(request, 'core/products/cart.html', {'cart': cart})
