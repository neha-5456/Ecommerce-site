from django.contrib import admin
from .models import Cart
from .models import Cartitems


class CartAdmin(admin.ModelAdmin):
      list_display = ["cart_id",  "date_added"]

class CartitemsAdmin(admin.ModelAdmin):
      list_display = ["product",  "cart" ,"user", "quantity" , "is_active"]
# Register your models here.
admin.site.register(Cart , CartAdmin)
admin.site.register(Cartitems , CartitemsAdmin)