from unicodedata import category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UsernameField 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
import json
import datetime

from django.urls import reverse

from store.forms import RegisterUserForm
from .models import *
from .utils import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, FormView
# Create your views here.

def search(request):
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     categories = Category.objects.all()
    
     if request.method == 'GET':
          query = request.GET.get('query')
          if query:
               products = Product.objects.filter(name__icontains=query,quantity__gt=0)
               paginator = Paginator(products, 12)
               pageN = request.GET.get('page')
               try:
                    products = paginator.page(pageN)
               except PageNotAnInteger:
                    products = paginator.page(1)
               except EmptyPage:
                    products = paginator.page(paginator.num_pages)
               context = {"products": products,'items':items, 'order':order,'cartItems':cartItems,'categories':categories, 'query':query}
               return render(request, 'search.html', context)
          else:
               print("No information to show")
               context = {'items':items, 'order':order,'cartItems':cartItems,'categories':categories}
               return render(request, 'search.html', context)


def productInfo(request, pk):
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     categories = Category.objects.all()

     product_info = Product.objects.get(id=pk)

     context = {"product_info": product_info,'items':items, 'order':order,'cartItems':cartItems,'categories':categories}
     return render(request, 'product.html',context)

def logout_user(request):
	logout(request)
	messages.success(request, ("You Were Logged Out!"))
	return redirect('store')

def register_user(request):
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     categories = Category.objects.all()

     if request.method == "POST":
          form = RegisterUserForm(request.POST)
          if form.is_valid():
               form.save()
               username = form.cleaned_data['username']
               password = form.cleaned_data['password1']
               user = authenticate(username=username,password=password)
               login(request, user)
               return redirect('store')
     else:
          form = RegisterUserForm()

     return render(request,'registration/register.html',{"form":form,'categories':categories,'cartItems':cartItems})

""" class ProfileView(LoginRequiredMixin, TemplateView):
     template_name = 'registration/profile.html' """

def profile(request):
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     categories = Category.objects.all()
     his_order = Order.objects.filter(customer=request.user,complete=True)
     ds=[]
     for i in his_order:
          ds.append({'date':i.date_ordered,'orderitem':OrderItem.objects.filter(order=i),'money':i.get_cart_total_buy})
     ds.reverse()
     context = {'items':items, 'order':order,'cartItems':cartItems,'categories':categories,'ds':ds}
     return render(request, 'registration/profile.html',context)


class SiteRegisterOkView(TemplateView):
     template_name = 'registration/register_ok.html' 

def store(request):
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     categories = Category.objects.all()

     category = request.GET.get('category')

     if category == None:
          product_info_list = Product.objects.filter(quantity__gt=0)
          nav = 'store'
          paginator = Paginator(product_info_list, 12)
          pageN = request.GET.get('page')
          try:
               products = paginator.page(pageN)
          except PageNotAnInteger:
               products = paginator.page(1)
          except EmptyPage:
               products = paginator.page(paginator.num_pages)

     else:
          product_info_list = Product.objects.filter(category__name=category,quantity__gt=0)
          nav = category
          paginator = Paginator(product_info_list, 12)
          pageN = request.GET.get('page')
          try:
               products = paginator.page(pageN)
          except PageNotAnInteger:
               products = paginator.page(1)
          except EmptyPage:
               products = paginator.page(paginator.num_pages)

     

     context = {'products':products,'cartItems':cartItems,'nav':nav,'categories':categories,'temo':category}
     return render(request,'store.html', context)

def cart(request):
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     categories = Category.objects.all()

     context = {'items':items,'order':order,'cartItems':cartItems,'categories':categories}
     return render(request, 'cart.html', context)

def checkout(request):
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     categories = Category.objects.all()

     context = {'items':items, 'order':order,'cartItems':cartItems,'categories':categories}
     return render(request, 'checkout.html', context)

def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']
     print('Action: ',action)
     print('Product:', productId)

     customer = request.user
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)

     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
     
     if action =='add':
          if orderItem.product.quantity >= orderItem.quantity+1:
               orderItem.quantity = (orderItem.quantity + 1)
          else:
               return JsonResponse('0', safe=False)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if orderItem.quantity <=0:
          orderItem.delete()

     return JsonResponse('Item was added', safe=False)


def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)

     customer = request.user
     order, created = Order.objects.get_or_create(customer=customer, complete=False)
     items = order.orderitem_set.all()

     total = float(data['form']['total'])
     order.transaction_id = transaction_id

     if total == float(order.get_cart_total):
          order.complete = True
     order.save()

     for i in items:
          product = Product.objects.get(id=i.product_id)
          product.quantity = product.quantity - i.quantity
          
          if(i.product.price < i.product.old_price):
               i.price_buy = i.product.price
          else:
               i.price_buy = i.product.old_price
          i.save()
     product.save()

     ShippingAddress.objects.create(
          customer=customer,
          order=order,
          address=data['shipping']['address'],
          city=data['shipping']['city'],
          telephoneNB=data['shipping']['telephoneNB'],
          zipcode=data['shipping']['zipcode'],
          )
     return JsonResponse("ok", safe=False)