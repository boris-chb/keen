from django import forms
from shop.models import Product



class CartAddProductForm(forms.ModelForm):
    # Overriding or Adding products
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
    class Meta:
        model = Product
        fields = ['quantity', 'size']
    