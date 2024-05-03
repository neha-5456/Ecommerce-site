from django.contrib import admin
from .models import Order , Payment , OrderProduct



class OrderAdmin(admin.ModelAdmin):
      list_display = ["id","user", "payment", "order_number", "first_name", "last_name", "phone", "email", "address_line_1", "address_line_2","country"
                      ,"state","city","order_note","order_total","tax","status","ip","is_order","create_at","update_at"]

class PaymentAdmin(admin.ModelAdmin):
      list_display = ["user",  "payment_id" ,"payment_method", "paid_amount" , "status", "created_at"]

class OrderProductAdmin(admin.ModelAdmin):
      list_display = ['user', 'payment', 'order', 'productprice', 'quantity', 'ordered']    
# Register your models here.
admin.site.register(Order , OrderAdmin)
admin.site.register(Payment , PaymentAdmin)
admin.site.register(OrderProduct , OrderProductAdmin)
# Register your models here.





