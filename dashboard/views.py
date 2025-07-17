from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from waste_logs.models import WasteLog
from recycle_tips.models import Tip
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard_view(request):
    # Get current user
    user = request.user
    
    # Get waste logs for the current user
    user_waste_logs = WasteLog.objects.filter(user=user)
    
    # Get recent logs (last 7 days)
    last_week = timezone.now() - timedelta(days=7)
    recent_logs = user_waste_logs.filter(date_created__gte=last_week).order_by('-date_created')[:5]
    
    # Get total waste by category
    waste_by_category = user_waste_logs.values('category__name').annotate(
        total=Sum('quantity_kg')
    ).order_by('-total')[:5]
    
    # Get recent recycling tips
    recent_tips = Tip.objects.order_by('-date_posted')[:3]
    
    # Total waste logged by user
    total_waste_logged = user_waste_logs.aggregate(total=Sum('quantity_kg'))['total'] or 0
    
    # Total number of logs
    total_logs = user_waste_logs.count()
    
    context = {
        'recent_logs': recent_logs,
        'waste_by_category': waste_by_category,
        'recent_tips': recent_tips,
        'total_waste_logged': total_waste_logged,
        'total_logs': total_logs,
    }
    
    return render(request, 'dashboard/dashboard.html', context)
