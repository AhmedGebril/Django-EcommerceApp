
from django.contrib import admin
from .models import Order,client,Product,OrderItem,ShippingAddress,Review

# Register your models here.
class OrdertTabular(admin.TabularInline):
    model = Order

class OrderItemTabular(admin.TabularInline):
    model = OrderItem

class ShippingTub(admin.TabularInline):
    model = ShippingAddress

class ReviewTub(admin.TabularInline):
    model = Review

@admin.register(client)
class myUserModel(admin.ModelAdmin):
    list_display = ['username', 'age', 'phone_number','description']
    list_display_links = ['username']
    inlines = [OrdertTabular,ReviewTub]

@admin.register(Order)
class Ordermodel (admin.ModelAdmin):
    list_display = ['user','created_at','status','tax_price','total_price','payment_method']
    inlines = [OrderItemTabular,ShippingTub]


@admin.register(Product)
class Productmodel (admin.ModelAdmin):
    search_fields = ['name__startswith']
    list_display = ['name','description','price']
    inlines = [OrderItemTabular,ReviewTub]
    list_per_page = 10
    list_filter = ['name', 'price']


@admin.register(OrderItem)
class OrderItemmodel (admin.ModelAdmin):
    list_display = ['product','order','quantity']




@admin.register(ShippingAddress)
class Shippingmodel(admin.ModelAdmin):
    list_display = ['street_address', 'city', 'state']


@admin.register(Review)
class ReviewModel(admin.ModelAdmin):
    list_display = ['user_id','rating','product_id','comment']




