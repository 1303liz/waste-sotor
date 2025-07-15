from django.contrib import admin
from .models import Tip

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_posted', 'author', 'display_content_type')
    list_filter = ('category', 'is_visual_guide', 'is_best_practice', 'is_tutorial', 'date_posted')
    search_fields = ('title', 'content', 'audience')
    date_hierarchy = 'date_posted'
    
    def display_content_type(self, obj):
        """Format the content type for admin display"""
        content_types = obj.get_content_type()
        if content_types:
            return ", ".join(content_types)
        return "Standard tip"
    
    display_content_type.short_description = 'Content Type'
