from django.db import models

from django.db import models
from django.contrib.auth.models import User

class WasteCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class WasteEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE)
    quantity_kg = models.FloatField()
    date_logged = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.quantity_kg}kg"
class WasteLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE)
    quantity_kg = models.FloatField()
    date_logged = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.quantity_kg}kg"