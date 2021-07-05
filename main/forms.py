from django import forms
from .models import School


class Subscribe(forms.Form):
    schools = School.objects.all()
    school = forms.ModelChoiceField(label="Schule", queryset=School.objects.all())
    name = forms.CharField(label="Name", max_length=200)
    email = forms.EmailField(label="E-Mail", max_length=200)
    # not needed for now - maybe later for sms messages
    # phone = forms.CharField(label="Telefon", max_length=200, required=0)

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get('email') and not cleaned_data.get('phone'):  # This will check for None or Empty
            raise forms.ValidationError('E-Mail oder Telefon muss angegeben werden')

        return cleaned_data


class Subscriptions(forms.Form):
    email = forms.EmailField(label="E-Mail", max_length=200, required=0)
