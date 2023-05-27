from django.db import models
from django.contrib.auth import get_user_model
from home.models import Product
from django.core import validators


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        ordering = ('paid', '-updated')

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            return int(total * (100 - self.discount)/100)
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(90)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return '{} valid from {} to {}'.format(self.code, self.valid_from, self.valid_to)