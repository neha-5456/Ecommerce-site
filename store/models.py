from django.db import models
from category.models import  Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField( max_length=50 , unique = True)
    slug = models.SlugField(max_length=100 , unique = True)
    description = models.TextField( max_length=255 )
    price = models.IntegerField( )
    stock = models.IntegerField()
    images = models.ImageField( upload_to='photos/products',blank= True , height_field=None, width_field=None, max_length=None)
    is_avilabel = models.BooleanField(default=True)
    category = models.ForeignKey(Category,  on_delete=models.CASCADE)
    created_date  = models.DateTimeField( auto_now_add = True)
    modified_date  = models.DateTimeField( auto_now = True)
   
    def get_absolute_url(self): 
         return reverse("product_detail_", args=[self.slug])   

  
 
    # class Meta:
    #     verbose_name = "category"
    #     verbose_name_plural = "categories"

    def __str__(self):
        return self.product_name
    
class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager , self).filter(is_active=True)
    def sizes(self):
        return super(VariationManager , self).filter(variation_category= 'size' ,is_active=True)
    def colors(self):
        return super(VariationManager , self).filter(variation_category= 'color' ,is_active=True)
        #return self.all().filter(variation_category = 'size')
    

Variant_category_choise = (
   ( 'color' ,'color'),
   ( 'size' ,'size'),

)

class Variation(models.Model): 
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    variation_category = models.CharField( max_length=50 , choices=  Variant_category_choise)
    variation_value = models.CharField( max_length=50 , unique = True)
    is_active = models.BooleanField(default=True)
    objects = VariationManager()
    created_date  = models.DateTimeField( auto_now_add = True)
    
    
    def __str__(self):
        return self.variation_value

    
