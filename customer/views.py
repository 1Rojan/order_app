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

  def get(self, request, *args, **kwargs):
    categories = Category.objects.all()
    return render(request, 'customer/place_order.html', {'categories':categories})

  def post(self, request, *args, **kwargs):
    order_items = []
    order_item_ids = request.POST.getlist('item[]')
    for item_id in order_item_ids:
      item = MenuItem.objects.get(pk__contains=item_id)
      item_data = {
        'pk':item.pk,
        'name':item.name,
        'price':item.price,
      }
      order_items.append(item_data)

    price = 0
    item_ids = []

    for item in order_items:
      item_ids.append(item['pk'])
      price += item['price']
    order = OrderModel.objects.create(price=price)
    order.item.add(*item_ids)

    context = {
      'orders': order
    }
    return render(request, 'customer/order_confirmation.html', context)

    


