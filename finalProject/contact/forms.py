from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        # fields = ['first_name', 'last_name', 'email', 'message'] # individual fields can be included this way as well
        fields = '__all__'  # includes all the fields from the model

        # widget attrs arguments allows us to add attributes (e.g., your own styles, placeholder) to our form input tags
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'style': 'padding: 15px'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message'})
        }
