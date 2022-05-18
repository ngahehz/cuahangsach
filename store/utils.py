import json
from .models import *

def cookieCart(request):
	cart = {}
	print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0}
	cartItems = order['get_cart_items']
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}