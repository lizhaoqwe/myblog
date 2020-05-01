from django import forms
from apps.forms import FormMixMin
class LoginForm(forms.Form,FormMixMin):
    telephone = forms.CharField(max_length=11,min_length=11)
    password = forms.CharField(max_length=200,min_length=6)