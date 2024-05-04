from django.shortcuts import render   , redirect 
from django.http import HttpResponse , JsonResponse
from cart.models import Cartitems
from .forms import OrderForm
from .models import Order , Payment , OrderProduct
from datetime import datetime
from store.models import Product , Variation
import json
# Create your views here.


def payment(request):
     body = json.loads(request.body)
     order = Order.objects.get(user = request.user , order_number = body['order_id'] , is_order = False)
     
     payment = Payment(
          user = request.user,
          payment_id =body['transId'],
          payment_method = body['payment_method'],
          paid_amount = order.order_total,
          status = body['status']
        ) 
     payment.save()
     order.payment = payment
     order.is_order = True
     order.save()
    
     # move the cartitems to OrderProduct
     cart_items =  Cartitems.objects.filter(user = request.user)
     for cart_item in cart_items :
        data = OrderProduct()
        data.order_id = order.id
        data.user_id = request.user.id
        data.payment = payment
        data.product_id = cart_item.product.id
        data.quantity = cart_item.quantity
        data.productprice = cart_item.product.price
     #    data.variation = cart_item.variations
        data.ordered = True
        data.save()
        items =  Cartitems.objects.get(id = cart_item.id)
        product_variatios = items.variations.all()
        data = OrderProduct.objects.get(id= data.id)
        data.variation.set(product_variatios)
        data.save()
       
        #reduce the product quantity souldout
        product = Product.objects.get(id= cart_item.product.id)
        product.stock -= 1 
        product.save()
         
        # clear cart 
        Cartitems.objects.filter(user = request.user).delete()
    
        # send order recived email  to the customer  -- pending

        # send order id and transaction back to send method via js  response
        data = {
          'order_number':order.order_number ,
          'trans_id':payment.payment_id
        }
        return  JsonResponse(data)

     # return render(request ,  'order/payments.html')


def placeorder(request , total=0 , quantity = 0 ):
   
    tax=0 
    grand_total =0
    curent_user = request.user
    cart_items =  Cartitems.objects.filter(user = curent_user  )
    for cart_item in cart_items :
            total += (cart_item.product.price * cart_item.quantity)
            quantity += (cart_item.quantity)
            tax = (2*total)/100
            grand_total = total+tax

    cartcount = cart_items.count()
    if cartcount <= 0 :
        return  redirect('store')
   
    if request.method == 'POST':
        
        form = OrderForm(request.POST)
        
        if form.is_valid():
            
            data = Order()
            data.user = curent_user
            data.first_name =  form.cleaned_data['first_name']
            data.last_name =  form.cleaned_data['last_name']
            data.phone =  form.cleaned_data['phone']
            data.email =  form.cleaned_data['email']
            data.address_line_1 =  form.cleaned_data['address_line_1']
            data.address_line_2 =  form.cleaned_data['address_line_2']
            data.country =  form.cleaned_data['country']
            data.state =  form.cleaned_data['state']
            data.city =  form.cleaned_data['city']
            data.order_note =  form.cleaned_data['order_note']
            data.order_total =  grand_total
            data.tax = tax
            data.ip =  request.META['REMOTE_ADDR']
            data.save()
         

            current_date = datetime.today().date()
            formatted_date = current_date.strftime('%Y%m%d')
            order_number = formatted_date + str(data.id)
            data.order_number = order_number 
            data.save()
            order = Order.objects.get(user = curent_user , is_order = False ,order_number = order_number)
            context = {
                 'order' : order ,
                 'cart_items' :cart_items,
                 "quantity" :quantity ,
                 "tax" : tax,
                 "grand_total":  grand_total,

            }
            return render(request ,  'order/payments.html', context)
    else:
         return redirect('checkout')
         



def order_complete(request):
   order_number = request.GET.get('order_number')
   trans_id =  request.GET.get('payment_id')
   try :
      order =  Order.objects.get(order_number = order_number ,is_order = True)
      payment = Payment.objects.get(payment_id = trans_id )
      orderproduct = OrderProduct.objects.filter(order_id = order.id)
      subtotal = 0 
      for item in orderproduct:
         subtotal += item.product.price * item.quantity

      context = {
         'order': order ,
         'orderproduct': orderproduct,
         'order_number' : order.order_number,
         'payment':payment,
         'trans_id' : payment.payment_id,
         'subtotal' : subtotal,
      }
      return render(request, 'order/order_complete.html', context)
   except(Order.doesNotExits ,Payment.doesNotExits ):
      return redirect('home')

   
   #   




