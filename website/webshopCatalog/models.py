from django.db import models

# Category model definning different categories that products can belong to. For example, drinks, steamed dimsum, pan fried dimsum...etc
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta keywords", max_length=255, help_text="Comma delimited words for SEO purpose")
    meta_description = models.CharField("Meta description", max_length=255, help_text="Content for meta tag description")
    #The auto_now_add will set the field datetime when the instance is called for the first time. User does not need to 
    #set this value
    created_at = models.DateTimeField(auto_now_add=True)
    #If the record is updated or saved, then datetime for updated_at field wwill automatically be added
    updated_at = models.DateTimeField(auto_now=True)
    #Prepare a dropdown list showing from which restaruant it will be possible to use this category. This
    #field is not intend to be used right now, but later in future should one have additional restaurants, it can be useful
    restaurants_choice = [('Hidden Dimsum 2900', ''),]
    available_restaurant = models.CharField("Available Restaurant", help_text="Select restaurant that uses this category", 
    choices=restaurants_choice)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Categories'
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ("catalog_category", (), {'category_slug' : self.slug})
    
