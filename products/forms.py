from django import forms
from .models import AboutUs, Category, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'bulk_pirce', 'category', 'type', 'image', 'instock', 'quantity_in_stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Product Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Product Price'}),
            'bulk_pirce': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bulk Price(optional)'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'instock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity in Stock'}),
        }

    # Optional: Add custom validation or helper methods if needed


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        
        
class AboutUsForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = [
            'company_name', 'description', 'description_de', 'location', 'latitude', 'longitude', 
            'email', 'phone', 'website', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'description_de': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
