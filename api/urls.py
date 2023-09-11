from django.urls import path
from .views import *


urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customers'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('orders/', OrderListCreateView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
