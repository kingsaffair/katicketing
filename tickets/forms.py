from django import forms
from django.forms import formset_factory

from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['fname', 'lname', 'price', 'payment_method']

TicketFormSet = formset_factory(TicketForm, extra=3)

