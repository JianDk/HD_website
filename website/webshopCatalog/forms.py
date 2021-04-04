from django import forms
from webshopCatalog.models import Product

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['created_at', 'updated_at']

    def clean_price(self):
        if self.cleaned_data['price'] < 0: #We allow 0 to be included in case we want to give out free products
            raise forms.ValidationError('Price cannot be negative value')
        return self.cleaned_data['price']

