from django.contrib import admin
from .models import *
from .forms import ProductAdminForm

# Register your models here.
class OrderItemUI(admin.ModelAdmin):
    list_display = ('order', 'product','quantity','price_buy')
    search_fields = ('order',)
class OrderUI(admin.ModelAdmin):
    list_display = ('customer', 'date_ordered','id','complete')
    list_filter = (('complete', admin.BooleanFieldListFilter),)
    search_fields = ('id',)
class ProductName(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'price','old_price','quantity')
    list_filter = ('category',('is_special', admin.BooleanFieldListFilter),'quantity',)
    search_fields = ('name',)
class ShippingAddressUI(admin.ModelAdmin):
    list_display = ('order', 'address','customer','telephoneNB')
    search_fields = ('order',)
admin.site.register(Category)
admin.site.register(Product,ProductName)
admin.site.register(Order,OrderUI)
admin.site.register(OrderItem,OrderItemUI)
admin.site.register(ShippingAddress,ShippingAddressUI)