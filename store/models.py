from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    old_price = models.DecimalField(max_digits=9,decimal_places=2,blank=True,default=0.00)
    price = models.DecimalField(max_digits=9,decimal_places=2,blank=True,default=0.00)
    author = models.CharField(max_length=200,null=True)
    image = models.ImageField(null=True,blank=True)
    description = models.TextField()
    is_special = models.BooleanField(default=False)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def sale_price(self):
        if self.old_price > self.price:
            return True
        return False

    def in_stock(self):
        if self.quantity>0:
            return True
        return False

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum ([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum ([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_total_buy(self):
        orderitems = self.orderitem_set.all()
        total = sum ([item.get_total_buy for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    price_buy = models.DecimalField(max_digits=9,decimal_places=2,blank=True,default=0.00, null=True)

    @property
    def get_total(self):
        if self.product.price < self.product.old_price:
            total = self.product.price * self.quantity
        else:
            total = self.product.old_price * self.quantity
        return total

    @property
    def get_total_buy(self):
        return self.price_buy * self.quantity

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    telephoneNB = models.CharField(max_length=10, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address