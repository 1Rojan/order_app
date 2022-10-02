from unicodedata import category
from django.shortcuts import redirect, render
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
    return render(request, 'customer/order.html', {'categories':categories})

  def post(self, request, *args, **kwargs):
    order_items = []
    order_item_ids = request.POST.getlist('items[]')
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
      order = OrderModel.objects.create(
      price=price,
      email=request.POST.get('email'),
      street=request.POST.get('street'),
      city=request.POST.get('city'),
      state=request.POST.get('state')
      )
      order.item.add(*item_ids)
      context = {
        'orders': order
      }

    return redirect('order_confirmation', pk=order.pk)
    

class OrderConfirmation(View):
  def get(self, request, pk, *args, **kwargs):
    order = OrderModel.objects.get(pk=pk)
    # context = {
    #   'pk':order.pk,
    #   'items':order.item,
    #   'price':order.price
    # }

    return render(request, 'customer/order_confirmation.html', {'orders':order, 'pk':order.pk})

  def post(self, request, pk, *args, **kwargs):
    import pdb
    pdb.set_trace()
    print(request.body)
    return redirect('payment_confirmation')


class OrderPayConfirmation(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'customer/order_pay_confirmatin.html')


