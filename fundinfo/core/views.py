from django.views.generic import View
from django.shortcuts import render
from .models import Product

class product_list_view(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, "core/products/list.html", {"products": products})
