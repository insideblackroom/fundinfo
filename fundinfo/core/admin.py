from .models import Product, Category
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    ...
    
class CategoryAdmin(admin.ModelAdmin):
    ...

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)