from django import forms
from django.forms import formset_factory

from .models import Guest

class TicketForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['fname', 'lname', 'price', 'payment_method']

TicketFormSet = formset_factory(TicketForm, extra=3)

