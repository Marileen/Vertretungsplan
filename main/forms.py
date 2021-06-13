from django import forms
from .models import School


class Subscribe(forms.Form):
    schools = School.objects.all()
    school = forms.ModelChoiceField(queryset=School.objects.all())

    name = forms.CharField(label="Name", max_length=200)
    email = forms.EmailField(label="E-Mail", max_length=200)
    phone = forms.CharField(label="Telefon", max_length=200)
