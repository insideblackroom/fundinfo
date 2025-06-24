from django.urls import path
from .views import product_list_view

app_name = "core"

urlpatterns = [
    path("products/", product_list_view.as_view(), name="product_list"),
]

