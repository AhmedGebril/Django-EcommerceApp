from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class client(models.Model):
    username = models.CharField(max_length=100, null=False, blank=False,default='')
    description = models.TextField(null=False, blank=False,default='')
    phone_number = models.CharField(max_length=15,default=0)
    age = models.IntegerField(null=False, blank=False,default=0)
    password = models.CharField(default=0,null=False,blank=False,max_length=100)
    isAdmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} - user_id {self.id}'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False,default='')
    description = models.TextField(null=False, blank=False,default='')
    price= models.IntegerField(null=False,blank=False,default=0)
    quantity = models.IntegerField(null=False,blank=False,default=0)
    brand = models.CharField(max_length=50,default='anything')
    category = models.CharField(max_length=50,default='anything')
    num_reviews = models.IntegerField(default=0)
    avg_rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    user = models.ForeignKey(client, on_delete=models.CASCADE,related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='unfinished',max_length=100)
    total_price = models.IntegerField(default=0)
    tax_price = models.DecimalField(max_digits=5, decimal_places=2, default=14)
    payment_method=models.CharField(max_length=50,default='visa/card')
    shipping_price = models.IntegerField(default=30)
    is_paid=models.BooleanField(default=False)
    paid_at=models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'id : {self.id} - status : {self.status}'



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='product_orderd')
    quantity = models.IntegerField(blank=False,null=False,default=0)

    def __str__(self):
        return f'product: {self.product.name} , product_price : {self.product.price}'

class ShippingAddress(models.Model):
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='shipping_addresses',default=7)

    def __str__(self):
        return f'{self.street_address}, {self.city}, {self.state}, {self.country}'

class Review(models.Model):
    user_id = models.ForeignKey(client,on_delete=models.CASCADE,related_name='user_reviews')
    comment = models.CharField(max_length=300,null=False,blank=False)
    product_id = models.ForeignKey(Product,models.CASCADE,related_name='product_review')
    rating = models.IntegerField(default=0,blank=False,null=False)

    def __str__(self):
        return f'username : {self.user_id.username} , product : {self.product_id.name} , rating : {self.rating}'
