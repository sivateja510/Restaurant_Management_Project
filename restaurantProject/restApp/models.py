from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import Permission

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_sold=models.IntegerField()    

    def __str__(self):
        return self.name

    
class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    waiter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=[('ordered', 'Ordered'), ('cooking', 'Cooking'), ('delivered', 'Delivered')], default='ordered')
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return self.item.price * self.quantity

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def createAuthToken(sender,instance,created, **kwargs):
    if created:
        Token.objects.create(user=instance)
