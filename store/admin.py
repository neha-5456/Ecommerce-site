from django.contrib import admin
from .models import Product , Variation

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}

    list_display = ("product_name",  "description" ,'category',"slug", 'created_date' )
# Register your models here.




class VariationAdmin(admin.ModelAdmin):
    list_display = ( "id" , "product" ,"variation_category", "variation_value", 'created_date',"is_active" )
    list_editable = ( 'is_active',)
    list_filter = ("variation_category", "variation_value", "product" ,'created_date',)

admin.site.register(Product, ProductAdmin)    
admin.site.register(Variation ,VariationAdmin )