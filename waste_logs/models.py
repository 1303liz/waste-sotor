from django.db import models
from django.contrib.auth.models import User

class BaseWasteLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.ForeignKey('WasteCategory', on_delete=models.CASCADE)
    quantity_kg = models.FloatField()
    date_logged = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class WasteEntry(BaseWasteLog):
    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.quantity_kg}kg"

class WasteLog(BaseWasteLog):
    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.quantity_kg}kg"

class WasteCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name