from django.db import models
from django.contrib.auth.models import User

class BaseTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('recyclables', 'Recyclables'),
            ('compostables', 'Compostables'),
            ('general_waste', 'General Waste'),
            ('plastic', 'Plastic'),
            ('organic', 'Organic'),
            ('e-waste', 'E-Waste'),
            ('general', 'General Sustainability')
        ]
    )
    date_posted = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_visual_guide = models.BooleanField(default=False, help_text="Is this tip a visual guide?")
    is_best_practice = models.BooleanField(default=False, help_text="Is this tip a best practice?")
    is_tutorial = models.BooleanField(default=False, help_text="Is this tip a tutorial?")

    class Meta:
        abstract = True
    
    def get_category_display(self):
        """Return the display name for the category"""
        return dict(self._meta.get_field('category').choices).get(self.category, self.category)

class Tip(BaseTip):
    image = models.ImageField(upload_to='recycle_tips/images/', null=True, blank=True, 
                             help_text="Upload an image to illustrate this tip")
    tutorial_steps = models.JSONField(null=True, blank=True, 
                                    help_text="JSON data for tutorial steps")
    audience = models.CharField(max_length=100, default="Community members", 
                              help_text="Target audience for this tip")
    
    class Meta:
        ordering = ['-date_posted']
    
    def __str__(self):
        return self.title
    
    def get_content_type(self):
        """Return the content type(s) of this tip as a list"""
        types = []
        if self.is_visual_guide:
            types.append("Visual Guide")
        if self.is_best_practice:
            types.append("Best Practice")
        if self.is_tutorial:
            types.append("Tutorial")
        return types
    
    @classmethod
    def get_category_choices(cls):
        """Return the list of category choices for templates"""
        return cls._meta.get_field('category').choices

