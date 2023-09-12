from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from .utils import send_sms_alert


# Create your views here.
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = (SessionAuthentication, OIDCAuthentication)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = (SessionAuthentication, OIDCAuthentication)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser]


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (SessionAuthentication, OIDCAuthentication)

    def perform_create(self, serializer):
        order = serializer.save()

        # get customer information associated with the order
        customer_name = order.customer.name
        recipient_phone = order.customer.phone_number
        order_item = order.item

        # send SMS alert to the customer
        send_sms_alert(customer_name, order_item, recipient_phone)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (SessionAuthentication, OIDCAuthentication)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser]
