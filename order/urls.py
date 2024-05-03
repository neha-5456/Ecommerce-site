
from django.urls import path
from order import views

urlpatterns = [
    path('place-order', views.placeorder, name='placeorder'),
    path('payment', views.payment, name='payment'),
    path('order-complete', views.order_complete, name='order_complete'),
    
]
