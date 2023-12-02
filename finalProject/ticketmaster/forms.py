from django import forms
from .models import Favorites_Library


class Favorites_Library_Form(forms.ModelForm):
    class Meta:
        model = Favorites_Library
        fields = '__all__'
