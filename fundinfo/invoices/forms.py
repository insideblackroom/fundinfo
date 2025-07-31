from .models import Invoice
from django import forms

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('address',)