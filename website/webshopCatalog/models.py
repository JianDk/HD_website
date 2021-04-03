from django.db import models
from django.db.models.fields.related import create_many_to_many_intermediary_model

class Product(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    description = models.TextField()
    allergic_note = models.CharField(max_length = 255)
    quantity = models.IntegerField(null = True, blank = True) #Used for campaign products to show how many items there is left
    price = models.DecimalField(max_digits=9, decimal_places=0, default=0.00)
    is_active = models.BooleanField(default = True)
    is_deliverable = models.BooleanField(default = True) 
    image_path = models.CharField(max_lenght = 255)
    meta_keywords = models.CharField(max_length=255, help_text="comma delimited keywords text for SEO")
    meta_description = models.CharField(max_length=255, help_text="SEO description content")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique = True,
    help_text="Unique text for url created from name")
    is_featured = models.BooleanField(default = False)
    is_bestseller = models.BooleanField(default=False)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ("catalog_product", (), {'product_slug' : self.slug})
    

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta keywords", max_length=255, help_text="Comma delimited words for SEO purpose")
    meta_description = models.CharField("Meta description", max_length=255, help_text="Content for meta tag description")
    #The auto_now_add will set the field datetime when the instance is called for the first time. User does not need to 
    #set this value
    created_at = models.DateTimeField(auto_now_add=True)
    #If the record is updated or saved, then datetime for updated_at field wwill automatically be added
    updated_at = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(Product)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ("catalog_category", (), {'category_slug' : self.slug})
    
    

        