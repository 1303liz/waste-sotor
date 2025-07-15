from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary using key in templates"""
    return dictionary.get(key, 0)
