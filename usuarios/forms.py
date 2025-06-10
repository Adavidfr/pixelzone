from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class LoginUsuarioForm(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           for campo in self.fields.values():
               campo.widget.attrs['class'] = 'form-control'
               campo.widget.attrs['style'] = 'background-color: #E8EAF2; color: #000;'
