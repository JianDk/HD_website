from django.contrib import admin

# Register your models here.
from webshopCatalog.models import Category, Product
from webshopCatalog.forms import ProductAdminForm

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    #How the admin site will list products
    list_display = ('name', 'price', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering =['-name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)

    #Sets up slug to be generated from product name
    prepopulated_fields = {'slug' : ('name',)}

#Registers the product model with the admin interface
admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    #sets up values for how admin site lists category
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)

    #Set up slug to be generated from category name
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Category, CategoryAdmin)


