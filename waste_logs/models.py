from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator
import uuid

class BaseWasteLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.ForeignKey('WasteCategory', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('WasteSubcategory', on_delete=models.SET_NULL, null=True, blank=True)
    quantity_kg = models.FloatField(validators=[MinValueValidator(0.0)])
    date_logged = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class WasteEntry(BaseWasteLog):
    """
    Individual waste entry that can be part of a waste log
    """
    waste_log = models.ForeignKey('WasteLog', on_delete=models.CASCADE, related_name='entries')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.quantity_kg}kg"

class WasteLog(BaseWasteLog):
    """
    Main waste logging entity that can contain multiple entries
    """
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(
        max_length=20, 
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('custom', 'Custom')
        ],
        blank=True,
        null=True
    )
    source = models.CharField(max_length=100, blank=True, null=True)
    measurement_method = models.CharField(
        max_length=50,
        choices=[
            ('estimated', 'Estimated'),
            ('weighed', 'Weighed'),
            ('counted', 'Counted'),
            ('calculated', 'Calculated')
        ],
        default='estimated'
    )
    
    def __str__(self):
        title_display = self.title if self.title else f"{self.category.name} log"
        return f"{self.user.username} - {title_display} - {self.date_logged.strftime('%Y-%m-%d')}"

class WasteCategory(models.Model):
    """
    Main waste categories
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True) 
    color = models.CharField(max_length=20, blank=True, null=True)
    is_recyclable = models.BooleanField(default=False)
    is_compostable = models.BooleanField(default=False)
    is_hazardous = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Waste Categories"
    
    def __str__(self):
        return self.name
        
class WasteSubcategory(models.Model):
    """
    Detailed subcategories for more precise waste classification
    """
    category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    recycling_instructions = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Waste Subcategories"
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"

class WasteAttachment(models.Model):
    """
    Media attachments for waste logs
    """
    waste_log = models.ForeignKey(WasteLog, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='waste_logs/attachments/')
    file_type = models.CharField(max_length=30, choices=[
        ('image', 'Image'),
        ('document', 'Document'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('other', 'Other')
    ])
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attachment for {self.waste_log}"

class WasteGoal(models.Model):
    """
    Personal waste reduction goals
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='waste_goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(WasteCategory, on_delete=models.SET_NULL, null=True, blank=True)
    target_quantity = models.FloatField(validators=[MinValueValidator(0.0)])
    current_quantity = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    unit = models.CharField(max_length=20, default='kg')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s Goal: {self.title}"
    
    @property
    def progress_percentage(self):
        """Calculate the progress percentage towards the goal"""
        if self.target_quantity == 0:
            return 100.0
        progress = (self.current_quantity / self.target_quantity) * 100
        return min(progress, 100.0)  # Cap at 100%
    
    @property
    def remaining_quantity(self):
        """Calculate the remaining quantity to reach the goal"""
        remaining = self.target_quantity - self.current_quantity
        return max(remaining, 0.0)  # Ensure non-negative value