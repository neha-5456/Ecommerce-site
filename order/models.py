from django.db import models

# Create your models here.
from django.db import models
from store.models import Product , Variation
from accounts.models import Account
# Create your models here.



class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField( max_length=100)
    payment_method = models.CharField( max_length=100)
    paid_amount = models.CharField( max_length=100)
    status = models.CharField( max_length=100)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
          ('New' , 'New'),
          ('Accepted' , 'Accepted'),
          ('Complted' , 'Complted'),
          ('Cancelled' , 'Cancelled')
         

    )
    user =  models.ForeignKey(Account, on_delete=models.SET_NULL , blank = True ,null =True)
    payment =  models.ForeignKey(Payment, on_delete=models.SET_NULL , blank = True ,null =True)
    order_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    address_line_1 = models.CharField(max_length=100)
    address_line_2  = models.CharField(max_length=100)
    country  = models.CharField(max_length=100)
    state  = models.CharField(max_length=100)
    city  = models.CharField(max_length=100)
    order_note  = models.CharField(max_length=100 ,null =True) 
    order_total  = models.FloatField()
    tax  = models.FloatField()
    status = models.CharField(max_length=50, choices =  STATUS ,default = 'New' )
    ip = models.CharField(max_length=50 ,blank = True ,null =True)
    is_order = models.BooleanField(default =False)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    user =  models.ForeignKey(Account, on_delete=models.CASCADE )
    payment =  models.ForeignKey(Payment, on_delete=models.CASCADE , blank = True ,null =True)
    order =  models.ForeignKey(Order, on_delete=models.CASCADE )
    product =  models.ForeignKey(Product, on_delete=models.CASCADE )
    variation =  models.ManyToManyField(Variation , blank = True)
    productprice = models.IntegerField()
    quantity = models.IntegerField()
    ordered = models.BooleanField(default =False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.product_name
    




   