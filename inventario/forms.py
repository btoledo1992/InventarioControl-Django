from django import forms
from .models import Producto
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'talle', 'color', 'precio', 'stock', 'foto']

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_staff'].label = 'Es administrador'
        self.fields['is_staff'].required = False
