from django.shortcuts import render , redirect ,HttpResponse , get_object_or_404
from store.models import Product , Variation
from .models import Cart
from .models import Cartitems
from accounts.models import Account
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import  login_required

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
        
    return cart


def add_cart(request , product_id):
     products = Product.objects.get(id=product_id)
     product_variation = []
     curent_user = request.user
     
     if request.user.is_authenticated:
        print("user")

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation =Variation.objects.get(product= products , variation_category__iexact = key , variation_value__iexact = value )
                    product_variation.append(variation)
                except:
                    pass
                        
         
        is_cart_exist = Cartitems.objects.filter( product = products , user = curent_user ).exists() 
    

        if is_cart_exist:
            cart_item = Cartitems.objects.filter( product = products , user = curent_user )
            
            ex_var_list = []
            id = []
            
            for item in cart_item:
                
                    existing_variation = item.variations.all()
                    
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)

            
        
            #    if product_variation in ex_var_list:
            #         print(ex_var_list)
            #         return HttpResponse('true')
            #    else:
            #         print(ex_var_list)
            #         return HttpResponse('false')
                

            if product_variation in ex_var_list:
                    #return HttpResponse('true')
                    #increase the cart item quantity
                    print('1sr if')
                    index = ex_var_list.index(product_variation)
                    item_id = id[index]
                    item = Cartitems.objects.get( product = products , id = item_id)
                    item.quantity += 1
                    item.save()
            else:
                    
                    print('1sr else')
                    item = Cartitems.objects.create(product = products , user = curent_user  , quantity  = 1)
                    if len(product_variation) > 0:
                        item.variations.clear() 
                        item.variations.add(*product_variation)
                    item.save()
        else:
                print('else')
                cart_item = Cartitems.objects.create(product = products , user = curent_user  , quantity  = 1)
                
                if len(product_variation) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
                    cart_item.save()

        #return HttpResponse(cart_item.variations.all)
        return redirect('cart')
     else:
            if request.method == 'POST':
                for item in request.POST:
                    key = item
                    value = request.POST[key]
                    
                    try:
                        variation =Variation.objects.get(product= products , variation_category__iexact = key , variation_value__iexact = value )
                        product_variation.append(variation)
                    except:
                        pass
                            
                            
            try:
                
                cart = Cart.objects.get(cart_id = _cart_id(request))

            except  Cart.DoesNotExist :
                    cart = Cart.objects.create( cart_id = _cart_id(request) ) 

            cart.save()

            
            is_cart_exist = Cartitems.objects.filter( product = products , cart = cart ).exists() 
        

            if is_cart_exist:
                cart_item = Cartitems.objects.filter( product = products , cart = cart )
                
                ex_var_list = []
                id = []
                
                for item in cart_item:
                    
                        existing_variation = item.variations.all()
                        
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                
            
                #    if product_variation in ex_var_list:
                #         print(ex_var_list)
                #         return HttpResponse('true')
                #    else:
                #         print(ex_var_list)
                #         return HttpResponse('false')
                    

                if product_variation in ex_var_list:
                        #return HttpResponse('true')
                        #increase the cart item quantity
                        print('1sr if')
                        index = ex_var_list.index(product_variation)
                        item_id = id[index]
                        item = Cartitems.objects.get( product = products , id = item_id)
                        item.quantity += 1
                        item.save()
                else:
                        
                        print('1sr else')
                        item = Cartitems.objects.create(product = products , cart = cart  , quantity  = 1)
                        if len(product_variation) > 0:
                            item.variations.clear() 
                            item.variations.add(*product_variation)
                        item.save()
            else:
                    print('else')
                    cart_item = Cartitems.objects.create(product = products , cart = cart  , quantity  = 1)
                    
                    if len(product_variation) > 0:
                        cart_item.variations.clear()
                        cart_item.variations.add(*product_variation)
                        cart_item.save()

            #return HttpResponse(cart_item.variations.all)
            return redirect('cart')
     
      
  
def cart(request , total=0 , quantity = 0 , cart_items = None , ):
    try:
        tax=0 
        grand_total =0
        if request.user.is_authenticated:
            cart_items = Cartitems.objects.all().filter(user =request.user , is_active = True)
            #cart_items = Cartitems.objects.filter( request.user , is_active = True) 
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = Cartitems.objects.filter( cart = cart , is_active = True) 
        
        for cart_item in cart_items :
            total += (cart_item.product.price * cart_item.quantity)
            quantity += (cart_item.quantity)
            tax = (2*total)/100
            grand_total = total+tax

    except ObjectDoesNotExist:  
          pass  
        
    context = {
        "total":total ,
        "cart_items" : cart_items,
        "quantity" :quantity ,
        "tax" : tax,
        "grand_total":  grand_total,
     }
    #return HttpResponse(cart_items['Product'])
    return render(request , 'store/cart.html' , context)


def remove_cart(request , product_id, cart_item_id):
     
     product = get_object_or_404(Product , id = product_id)
     try:
            if request.user.is_authenticated:
                 cart_item = Cartitems.objects.get( product = product , user = request.user , id = cart_item_id)
                 
            else:   
                cart = Cart.objects.get(cart_id = _cart_id(request))  
                cart_item = Cartitems.objects.get( product = product , cart = cart , id = cart_item_id)
            if cart_item.quantity >1 :
                    cart_item.quantity -= 1
                    cart_item.save()
            else :
                    cart_item.delete()       
     except:
          pass     

     return redirect('cart')     


def  remove_cart_items(request , product_id , cart_item_id):
    
     product = get_object_or_404(Product , id = product_id)
     try:
        if request.user.is_authenticated:
             cart_item = Cartitems.objects.get( product = product , user = request.user , id= cart_item_id )
            
        else:
             cart = Cart.objects.get(cart_id = _cart_id(request))
             cart_item = Cartitems.objects.get( product = product , cart = cart , id= cart_item_id )
        cart_item.delete()     
     except :
          pass   
     return redirect('cart') 





@login_required(login_url='login')
def checkout(request , total=0 , quantity = 0 , cart_items = None):
    try:
        tax=0 
        grand_total =0
        if request.user.is_authenticated:
            cart_items = Cartitems.objects.all().filter(user =request.user , is_active = True)
            #cart_items = Cartitems.objects.filter( request.user , is_active = True) 
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = Cartitems.objects.filter( cart = cart , is_active = True) 
        for cart_item in cart_items :
            total += (cart_item.product.price * cart_item.quantity)
            quantity += (cart_item.quantity)
        tax = (2*total)/100
        grand_total = total+tax

    except ObjectDoesNotExist:
        pass  
        
    context = {
        "total":total ,
        "cart_items" : cart_items,
        "quantity" :quantity ,
        "tax" : tax,
        "grand_total":  grand_total,
     } 
    return render(request, 'store/checkout.html' , context)
     
     
          
     


