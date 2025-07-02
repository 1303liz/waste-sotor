from django.db import models

class BaseTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('plastic', 'Plastic'),
            ('organic', 'Organic'),
            ('e-waste', 'E-Waste'),
            ('general', 'General Sustainability')
        ]
    )
    date_posted = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Tip(BaseTip):
    def __str__(self):
        return self.title

