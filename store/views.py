from django.shortcuts import render , get_object_or_404
from store.models import Product
from category.models import Category
from cart.models import Cartitems
from cart.views import _cart_id
# Create your views here.

def product_detail(request , category_slug = None , product_slug = None):
     try :
          single_product = Product.objects.get(category__slug = category_slug , slug = product_slug )
          in_cart = Cartitems.objects.filter(cart__cart_id = _cart_id(request) , product =single_product ).exists() 
          
     except Exception as e :
          raise e


     context = {
        'single_product': single_product,
         'in_cart' : in_cart, 
          }
     return render(request, 'store/product_detail.html'  , context)




def  store(request , category_slug = None):  
     categories = None 
     products = None

     if category_slug != None :
          categories = get_object_or_404(Category ,  slug  = category_slug)
          products = Product.objects.select_related('category').filter(category = categories , is_avilabel=True).all()
          product_count = products.count()
     else:
          products = Product.objects.select_related('category').filter(is_avilabel=True).all()
         # products = Product.objects.all().filter(is_avilabel=True).values()
          product_count = products.count()
     context = {
    'products': products,
    'product_count':product_count,
     }
 
    
     return render(request, 'store/store.html' , context)


     