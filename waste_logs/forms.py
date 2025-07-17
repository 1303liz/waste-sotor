from django import forms
from django.core.validators import MinValueValidator
from .models import WasteLog, WasteEntry, WasteAttachment, WasteGoal, WasteCategory, WasteSubcategory
from django.utils.translation import gettext_lazy as _

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class DateInput(forms.DateInput):
    input_type = 'date'

class WasteLogForm(forms.ModelForm):
    """Form for creating and editing waste logs"""
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
        # Add a dependent dropdown for subcategories
        self.fields['subcategory'].queryset = WasteSubcategory.objects.none()
        
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = WasteSubcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.category:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.all()
    
    class Meta:
        model = WasteLog
        fields = [
            'title', 'category', 'subcategory', 'quantity_kg', 
            'date_logged', 'description', 'location',
            'measurement_method', 'is_recurring', 'recurrence_pattern'
        ]
        widgets = {
            'date_logged': DateTimeInput(),
            'description': forms.Textarea(attrs={'rows': 3}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'quantity_kg': _('Enter the weight in kilograms'),
            'is_recurring': _('Check if this is a recurring waste event'),
            'location': _('Optional: Enter the location where the waste was generated'),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance

class WasteEntryForm(forms.ModelForm):
    """Form for adding entries to a waste log"""
    
    class Meta:
        model = WasteEntry
        fields = ['category', 'subcategory', 'quantity_kg', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.waste_log = kwargs.pop('waste_log', None)
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
        # Add dependent dropdown for subcategories
        self.fields['subcategory'].queryset = WasteSubcategory.objects.none()
        
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = WasteSubcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.category:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.all()
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if self.waste_log:
            instance.waste_log = self.waste_log
        if commit:
            instance.save()
        return instance

class WasteAttachmentForm(forms.ModelForm):
    """Form for adding attachments to waste logs"""
    
    class Meta:
        model = WasteAttachment
        fields = ['file', 'file_type', 'title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            if field_name != 'file':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control-file'})

class WasteGoalForm(forms.ModelForm):
    """Form for creating and editing waste goals"""
    
    class Meta:
        model = WasteGoal
        fields = [
            'title', 'description', 'category', 
            'target_quantity', 'unit', 
            'start_date', 'end_date'
        ]
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance

class DateRangeFilterForm(forms.Form):
    """Form for filtering waste logs by date range"""
    start_date = forms.DateField(
        widget=DateInput(attrs={'class': 'form-control'}),
        required=False
    )
    end_date = forms.DateField(
        widget=DateInput(attrs={'class': 'form-control'}),
        required=False
    )
    category = forms.ModelChoiceField(
        queryset=WasteCategory.objects.all(),
        empty_label="All Categories",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
