from django import forms


class Subscribe(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    email = forms.EmailField(label="E-Mail", max_length=200)
    phone = forms.CharField(label="Telefon", max_length=200)
