from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from unittest.mock import patch, MagicMock

import api.utils
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from .utils import send_sms_alert


# Create your tests here.
class CustomerTestCase(TestCase):
    def setUp(self):
        # self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')

    def test_create_customer(self):
        url = reverse('customers')
        data = {'name': 'Booora', 'email': 'booora@gmail.com', 'code': 'CQ111', 'phone_number': '+254720770571'}
        # self.client.post(reverse('oidc_authentication_init'))
        # self.client.login(username='testuser', password='testpassword')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.get().name, 'Booora')
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().email, 'booora@gmail.com')


class OrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name='Booora', email='booora@gmail.com', code='CDW1212')

    def test_create_order(self):
        url = reverse('orders')
        data = {'customer': self.customer.id, 'item': 'test item', 'amount': 2000.00, 'time': '2023-09-12T16:34:00Z'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().customer, self.customer)
        self.assertEqual(Order.objects.get().item, 'test item')
        self.assertEqual(Order.objects.get().amount, 2000.00)


class SMSTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name='Booora', email='booora@gmail.com', code='CDW2121',
                                                phone_number='+254720770571')

    @patch('api.utils.send_sms_alert')
    def test_send_sm_alert(self, mock_send_sms_alert):
        url = reverse('orders')
        data = {'customer': self.customer.id, 'item': 'item 2', 'amount': 2000.0, 'time': '2023-09-12T16:34:00Z'}

        # mock response for the sms function
        mock_send_sms_alert.return_value = MagicMock()

        # send post request to create order
        response = self.client.post(url, data, format='json')

        # assert sms function was called with expected args
        # mock_send_sms_alert.assert_called_once_with(
        #     customer_name=self.customer.name,
        #     order_item=data['item'],
        #     recipient_phone=self.customer.phone_number
        # )
        send_sms_alert(
            customer_name=self.customer.name,
            order_item=data['item'],
            recipient_phone=self.customer.phone_number
        )

        # assert response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().item, 'item 2')
