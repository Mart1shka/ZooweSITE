# forms.py
from django import forms
from .models import Product
from .models import CartItem

class CartAddProductForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'currency']



