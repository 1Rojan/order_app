from unicodedata import category
from django.shortcuts import render
from django.urls import conf
from django.views import View

from customer.models import Category, MenuItem, OrderModel


class Index(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'customer/index.html')

  
class About(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'customer/about.html')


class Order(View):
  def get(self, request,*args, **kwargs):
  #   categories = Category.objects.all()
  #   context = {}
  #   for category in categories:
  #     name = category.name
  #     name1 = MenuItem.objects.filter(category__name__contains=name)
  #     context[name] = name1
  #   return render(request, 'customer/order.html', context)

    appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
    entres = MenuItem.objects.filter(category__name__contains='Antre')
    desserts = MenuItem.objects.filter(category__name__contains='Dessert')
    drinks = MenuItem.objects.filter(category__name__contains='Drink')

    context= {
      'appetizers': appetizers,
      'entres': entres,
      'desserts':desserts,
      'drinks':drinks
    }

    return render(request, 'customer/order.html', context)


  def post(self, request, *args, **kwargs):
    order_items = {
      'items':[]
    }
    items = request.POST.getlist('items[]')
    for item in items:
      menu_item = MenuItem.objects.get(pk__contains=int(item))
      item_data = {
        'id': menu_item.pk,
        'name': menu_item.name,
        'price': menu_item.price  
      }
      order_items['items'].append(item_data)

      price = 0
      item_ids = []

      for item in order_items['items']:
        price +=item['price']
        item_ids.append(item['id'])
      
      order = OrderModel.objects.create(price=price)
      order.item.add(*item_ids)

      context = {
        'items': order_items['items'],
        'price': price
      }

    return render(request, 'customer/order_confirmation.html', context)