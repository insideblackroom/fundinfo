from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("products/", views.product_list_view.as_view(), name="product_list"),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('cart/add/quantity/<int:id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/add/<int:id>/', views.cart_append, name='cart_append'),
    path('cart/remove/<int:id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('cart/empty/', views.EmptyCartView.as_view(), name='cart_empty'),
    path('cart/', views.ShowCartView.as_view(), name='cart')
]

