from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RecyclingFacilitator(models.Model):
    """
    Organizations or businesses that facilitate the recycling process
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to='facilitators/logos/', blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class RecyclingProcess(models.Model):
    """
    Detailed information about recycling processes for specific waste categories
    """
    facilitator = models.ForeignKey(RecyclingFacilitator, on_delete=models.CASCADE, related_name='processes')
    waste_category = models.ForeignKey('waste_logs.WasteCategory', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    steps = models.TextField(help_text="Detailed steps of the recycling process")
    output_products = models.TextField(blank=True, null=True, help_text="Products created from this recycling process")
    environmental_impact = models.TextField(blank=True, null=True, help_text="Environmental benefits of this process")
    image = models.ImageField(upload_to='facilitators/processes/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Recycling Processes"
    
    def __str__(self):
        return f"{self.facilitator.name} - {self.waste_category.name} process"

class FacilitatorCollection(models.Model):
    """
    Records of waste collected by facilitators
    """
    facilitator = models.ForeignKey(RecyclingFacilitator, on_delete=models.CASCADE, related_name='collections')
    waste_category = models.ForeignKey('waste_logs.WasteCategory', on_delete=models.CASCADE)
    quantity_kg = models.FloatField()
    collection_date = models.DateField()
    source_location = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.facilitator.name} collected {self.quantity_kg}kg of {self.waste_category.name}"

class RecyclingImpactMetric(models.Model):
    """
    Environmental impact metrics for recycling activities
    """
    facilitator = models.ForeignKey(RecyclingFacilitator, on_delete=models.CASCADE, related_name='impact_metrics')
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()
    unit = models.CharField(max_length=50)
    date_recorded = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    
    METRIC_TYPES = [
        ('co2_saved', 'CO2 Emissions Saved'),
        ('water_saved', 'Water Saved'),
        ('energy_saved', 'Energy Saved'),
        ('landfill_reduced', 'Landfill Waste Reduced'),
        ('trees_saved', 'Trees Saved'),
        ('other', 'Other')
    ]
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    
    def __str__(self):
        return f"{self.facilitator.name} - {self.get_metric_type_display()}: {self.metric_value} {self.unit}"
