from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    code = models.CharField(max_length=10)
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField()

    def __str__(self):
        return 'Order {self.id} for {self.customer.name}'
