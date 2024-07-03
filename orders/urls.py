from django.urls import path
from . import views
from .views import stripe_webhook

urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('orders/', views.order_list_view, name='order_list_view'),
    path('orders/<int:order_id>/', views.order_detail_view, name='order_detail_view'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),


    
]
"""from django.urls import path
from .views import CartView, CheckoutView, OrderListView, OrderDetailView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order_list/', OrderListView.as_view(), name='order_list'),
    path('order_detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]
# orders/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cartview.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order_list/', views.OrderListView.as_view(), name='order_list'),
    path('order_detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
] """
