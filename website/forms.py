from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('COD', 'Cash on Delivery')
)

class CheckoutForm(forms.Form):
    apartment_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':"Apartment or suite"
    })) 
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':"1234 Main St"
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class' : "custom-select d-block w-100"
        }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class' : "form-control"
    }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect,choices= PAYMENT_CHOICES)