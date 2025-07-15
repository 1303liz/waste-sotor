from django import forms
from .models import Tip
import json

class TipForm(forms.ModelForm):
    tutorial_steps_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False,
        help_text="Enter tutorial steps, one per line. These will be converted to a structured format."
    )
    
    class Meta:
        model = Tip
        fields = ['title', 'content', 'category', 'image', 
                  'is_visual_guide', 'is_best_practice', 'is_tutorial',
                  'audience']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'audience': forms.TextInput(attrs={'class': 'form-control'}),
            'is_visual_guide': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_best_practice': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_tutorial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_tutorial_steps_text(self):
        """Convert tutorial steps from text to JSON format"""
        steps_text = self.cleaned_data.get('tutorial_steps_text', '')
        is_tutorial = self.cleaned_data.get('is_tutorial', False)
        
        if is_tutorial and steps_text:
            # Split by line and remove empty lines
            steps = [step.strip() for step in steps_text.split('\n') if step.strip()]
            
            # Create a JSON structure with steps
            tutorial_data = {
                'steps': [{'number': i+1, 'description': step} for i, step in enumerate(steps)]
            }
            
            return tutorial_data
        elif is_tutorial:
            return {'steps': []}
        else:
            return None
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Process tutorial steps
        tutorial_steps = self.cleaned_data.get('tutorial_steps_text')
        if tutorial_steps is not None:
            instance.tutorial_steps = tutorial_steps
        
        if commit:
            instance.save()
        
        return instance
