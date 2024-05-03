from django.shortcuts import render
from store.models import Product

def  home(request):
    products = Product.objects.select_related('category').all()
    #products = Product.objects.filter(is_avilabel=True).values()
      
    context = {
    'products': products,
     }
     
 
    return render(request, 'home.html' , context)


# def  store(request):    
#     return render(request, 'store.html')