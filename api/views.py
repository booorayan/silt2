from rest_framework import generics
from rest_framework import permissions

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer


# Create your views here.
class CustomerListCreateView(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
