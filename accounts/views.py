from django.shortcuts import render , redirect , HttpResponse
from .forms import RegistrationForm

from django.contrib import messages ,auth
from .models import Account
from cart.models import Cart ,Cartitems
from cart.views import _cart_id


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            

            user =  Account.objects.create_user(email = email, first_name =first_name , last_name= last_name  , password= password )
            user.phone = phone 
            user.save()
    else:    
        form = RegistrationForm()


    context = {
            'form': form,
        
        }
    return  render(request , 'accounts/register.html', context)


def login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

       
        user =  auth.authenticate(email= email , password = password)
        
        if user is not None:
 
            try:
                
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_exist = Cartitems.objects.filter( cart = cart ).exists() 
                if is_cart_exist:
                    cart_items = Cartitems.objects.filter( cart = cart , is_active = True) 
                    product_variation = []
                    for item in cart_items :
                        variations = item.variations.all()
                        product_variation.append(list(variations))
                       
                    cart_item = Cartitems.objects.filter(  user = user )
            
                    ex_var_list = []
                    id = []
            
                    for item in cart_item:
                        
                            existing_variation = item.variations.all()
                            
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)
                    for pr in product_variation:
                            if pr in ex_var_list:
                                   index = ex_var_list.index(pr)
                                   item_id = id[index]
                                   item = Cartitems.objects.get(  user = user, id = item_id)
                                   item.user = user
                                   item.quantity += 1
                                   item.save()

                            else:
                                 
                                cart_item = Cartitems.objects.filter(cart = cart  )
                                for item in cart_item:
                                    item.user = user
                                    item.save()                   


            except:
                
                pass


            auth.login(request , user)
            messages.success(request , "user is successfully loged in")
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print('query->' , query)
                params = dict(x.split('=') for x in query.split('&') )
                print('params->' , params)
                if 'next' in params:
                     nextPage = params['next']
                     return redirect(nextPage)
                     
                
            except:
                 return redirect('dashboard')
        else:
            messages.error(request , "something went wrong")
            return redirect('login')
            
    return  render(request , 'accounts/login.html')



def dashboard(request):
    return  render(request , 'dashboard.html')


def logout(request):
    auth.logout(request)
    messages.success(request , "logout successfully ")
    return redirect('login')
