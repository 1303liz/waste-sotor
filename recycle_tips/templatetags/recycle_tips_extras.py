from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Template filter to get an item from a dictionary using a key"""
    return dictionary.get(key, 0)

@register.filter
def sum_values(value):
    """Template filter to sum the values of a dictionary or iterable"""
    if hasattr(value, 'values'):
        # If it's a dictionary, sum its values
        return sum(value.values())
    elif hasattr(value, '__iter__'):
        # If it's an iterable, sum its items
        return sum(value)
    return 0
