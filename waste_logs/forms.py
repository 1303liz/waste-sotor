from django import forms
from .models import WasteLog

class WasteLogForm(forms.ModelForm):
    class Meta:
        model = WasteLog
        fields = ['category', 'quantity_kg']
