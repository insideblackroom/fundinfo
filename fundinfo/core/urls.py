from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("products/", views.product_list_view.as_view(), name="product_list"),
    path('cart/add/<int:id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('cart/empty/', views.EmptyCartView.as_view(), name='cart_empty'),
    path('cart/', views.ShowCartView.as_view(), name='cart')
]

