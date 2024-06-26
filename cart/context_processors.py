from .models import Cart ,Cartitems 
from .views import _cart_id

def counter(request):
    cart_count = 0
    if 'admin' in request.path :
      return {}
    else:
       try: 
            cart  =  Cart.objects.filter(cart_id = _cart_id(request))
            if request.user.is_authenticated:
                cart_items = Cartitems.objects.all().filter(user =request.user )
            else:   
              cart_items = Cartitems.objects.all().filter(cart = cart[:1])
            for cart_items in cart_items :
                cart_count += cart_items.quantity
       except  Cartitems.DoesNotExist :
           cart_count = 0
    return dict(cart_count = cart_count)       