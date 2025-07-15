from django import template
from django.utils.safestring import mark_safe
import datetime

register = template.Library()

@register.simple_tag
def terminal_status_message(message, status='info'):
    """
    Return a terminal-style status message with appropriate coloring based on status
    """
    colors = {
        'success': '#28a745',  # green
        'info': '#17a2b8',     # blue
        'warning': '#ffc107',  # yellow
        'error': '#dc3545',    # red
    }
    
    color = colors.get(status, colors['info'])
    prefix = {
        'success': '✅ SUCCESS',
        'info': 'ℹ️ INFO',
        'warning': '⚠️ WARNING',
        'error': '❌ ERROR',
    }.get(status, 'ℹ️ INFO')
    
    now = datetime.datetime.now().strftime('%H:%M:%S')
    
    html = f"""
    <div class="terminal-line">
        <span class="terminal-time">[{now}]</span>
        <span class="terminal-status" style="color: {color}">{prefix}:</span>
        <span class="terminal-message">{message}</span>
    </div>
    """
    
    return mark_safe(html)
