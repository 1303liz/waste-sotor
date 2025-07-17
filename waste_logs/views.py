from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Sum, Avg, Count, F, Q
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay
from django.core.paginator import Paginator
import json
from datetime import datetime, timedelta

from .models import (
    WasteLog, WasteEntry, WasteAttachment, 
    WasteGoal, WasteCategory, WasteSubcategory
)
from .forms import (
    WasteLogForm, WasteEntryForm, WasteAttachmentForm,
    WasteGoalForm, DateRangeFilterForm
)

@login_required
def index(request):
    """Main waste logs dashboard view"""
    # Get filter parameters
    filter_form = DateRangeFilterForm(request.GET)
    filters = Q(user=request.user)
    
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('start_date'):
            filters &= Q(date_logged__gte=filter_form.cleaned_data['start_date'])
        if filter_form.cleaned_data.get('end_date'):
            filters &= Q(date_logged__lte=filter_form.cleaned_data['end_date'])
        if filter_form.cleaned_data.get('category'):
            filters &= Q(category=filter_form.cleaned_data['category'])
    
    # Recent waste logs
    logs = WasteLog.objects.filter(filters).order_by('-date_logged')
    
    # Pagination for waste logs
    paginator = Paginator(logs, 10)  # Show 10 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Summary statistics
    total_waste = logs.aggregate(total=Sum('quantity_kg'))['total'] or 0
    logs_count = logs.count()
    
    # Recent goals
    goals = WasteGoal.objects.filter(
        user=request.user,
        is_completed=False
    ).order_by('end_date')[:3]
    
    # Category breakdown
    category_breakdown = logs.values('category__name', 'category__color') \
                            .annotate(total=Sum('quantity_kg')) \
                            .order_by('-total')
    
    # Time series data for chart (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    time_series = logs.filter(date_logged__gte=thirty_days_ago) \
                     .annotate(date=TruncDay('date_logged')) \
                     .values('date') \
                     .annotate(total=Sum('quantity_kg')) \
                     .order_by('date')
    
    time_series_data = {
        'labels': [entry['date'].strftime('%Y-%m-%d') for entry in time_series],
        'data': [float(entry['total']) for entry in time_series]
    }
    
    context = {
        'page_obj': page_obj,
        'total_waste': total_waste,
        'logs_count': logs_count,
        'goals': goals,
        'category_breakdown': category_breakdown,
        'time_series_data': json.dumps(time_series_data),
        'filter_form': filter_form
    }
    
    return render(request, 'waste_logs/home.html', context)

@login_required
def report(request):
    """Create a new waste log"""
    if request.method == 'POST':
        form = WasteLogForm(request.POST, user=request.user)
        if form.is_valid():
            waste_log = form.save()
            messages.success(request, 'Waste log created successfully.')
            return redirect('waste_logs_home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = WasteLogForm(user=request.user)
    
    # Get categories for the form
    categories = WasteCategory.objects.all()
    
    context = {
        'form': form,
        'categories': categories
    }
    
    return render(request, 'waste_logs/report.html', context)

@login_required
def waste_log_detail(request, log_id):
    """View for a single waste log with its entries and attachments"""
    waste_log = get_object_or_404(WasteLog, pk=log_id)
    
    # Security check - only the owner can see the log
    if waste_log.user != request.user:
        messages.error(request, "You don't have permission to view this waste log.")
        return redirect('waste_logs_home')
    
    entries = waste_log.entries.all().order_by('-date_logged')
    attachments = waste_log.attachments.all().order_by('-uploaded_at')
    
    # Attachment form
    if request.method == 'POST':
        attachment_form = WasteAttachmentForm(request.POST, request.FILES)
        if attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.waste_log = waste_log
            attachment.save()
            messages.success(request, 'Attachment added successfully.')
            return redirect('waste_log_detail', log_id=log_id)
    else:
        attachment_form = WasteAttachmentForm()
    
    context = {
        'waste_log': waste_log,
        'entries': entries,
        'attachments': attachments,
        'attachment_form': attachment_form,
    }
    
    return render(request, 'waste_logs/waste_log_detail.html', context)

@login_required
def edit_waste_log(request, log_id):
    """Edit an existing waste log"""
    waste_log = get_object_or_404(WasteLog, pk=log_id)
    
    # Security check - only the owner can edit the log
    if waste_log.user != request.user:
        messages.error(request, "You don't have permission to edit this waste log.")
        return redirect('waste_logs_home')
    
    if request.method == 'POST':
        form = WasteLogForm(request.POST, instance=waste_log, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Waste log updated successfully.')
            return redirect('waste_log_detail', log_id=log_id)
    else:
        form = WasteLogForm(instance=waste_log, user=request.user)
    
    context = {
        'form': form,
        'waste_log': waste_log,
        'is_edit': True
    }
    
    return render(request, 'waste_logs/report.html', context)

@login_required
def delete_waste_log(request, log_id):
    """Delete a waste log"""
    waste_log = get_object_or_404(WasteLog, pk=log_id)
    
    # Security check - only the owner can delete the log
    if waste_log.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this waste log.")
    
    if request.method == 'POST':
        waste_log.delete()
        messages.success(request, 'Waste log deleted successfully.')
        return redirect('waste_logs_home')
    
    return render(request, 'waste_logs/delete_waste_log.html', {'waste_log': waste_log})

@login_required
def add_waste_entry(request, log_id):
    """Add an entry to an existing waste log"""
    waste_log = get_object_or_404(WasteLog, pk=log_id)
    
    # Security check - only the owner can add entries
    if waste_log.user != request.user:
        messages.error(request, "You don't have permission to add entries to this waste log.")
        return redirect('waste_logs_home')
    
    if request.method == 'POST':
        form = WasteEntryForm(request.POST, user=request.user, waste_log=waste_log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry added successfully.')
            return redirect('waste_log_detail', log_id=log_id)
    else:
        form = WasteEntryForm(user=request.user, waste_log=waste_log)
    
    context = {
        'form': form,
        'waste_log': waste_log
    }
    
    return render(request, 'waste_logs/add_waste_entry.html', context)

@login_required
def get_subcategories(request):
    """AJAX view to get subcategories for a category"""
    category_id = request.GET.get('category_id')
    subcategories = list(WasteSubcategory.objects.filter(
        category_id=category_id).values('id', 'name'))
    return JsonResponse({'subcategories': subcategories})

@login_required
def analytics(request):
    """Waste analytics dashboard"""
    # Date range filter
    filter_form = DateRangeFilterForm(request.GET)
    filters = Q(user=request.user)
    
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('start_date'):
            filters &= Q(date_logged__gte=filter_form.cleaned_data['start_date'])
        if filter_form.cleaned_data.get('end_date'):
            filters &= Q(date_logged__lte=filter_form.cleaned_data['end_date'])
        if filter_form.cleaned_data.get('category'):
            filters &= Q(category=filter_form.cleaned_data['category'])
    
    # Default to last 6 months if no date filter
    if not filter_form.cleaned_data.get('start_date'):
        six_months_ago = timezone.now() - timedelta(days=180)
        filters &= Q(date_logged__gte=six_months_ago)
    
    logs = WasteLog.objects.filter(filters)
    
    # Summary statistics
    stats = {
        'total_waste': logs.aggregate(total=Sum('quantity_kg'))['total'] or 0,
        'avg_per_day': logs.aggregate(avg=Avg('quantity_kg'))['avg'] or 0,
        'logs_count': logs.count(),
    }
    
    # Category breakdown
    category_data = logs.values('category__name', 'category__color') \
                       .annotate(total=Sum('quantity_kg')) \
                       .order_by('-total')
    
    # Monthly trend
    monthly_trend = logs.annotate(month=TruncMonth('date_logged')) \
                        .values('month') \
                        .annotate(total=Sum('quantity_kg')) \
                        .order_by('month')
    
    # Weekly trend
    weekly_trend = logs.annotate(week=TruncWeek('date_logged')) \
                      .values('week') \
                      .annotate(total=Sum('quantity_kg')) \
                      .order_by('week')
    
    # Top waste types
    top_waste = logs.values('category__name') \
                   .annotate(total=Sum('quantity_kg')) \
                   .order_by('-total')[:5]
    
    # Environmental impact estimation (simplified)
    total_kg = stats['total_waste']
    
    # Simple estimations - would be more complex in a real app
    impact = {
        'co2_equivalent': total_kg * 2.5,  # Simplified CO2 equivalent
        'landfill_volume': total_kg * 0.001,  # Simplified landfill volume in m³
        'trees_saved': total_kg * 0.02 if logs.filter(category__name__icontains='paper').exists() else 0,
    }
    
    # Chart data preparation
    monthly_data = {
        'labels': [entry['month'].strftime('%b %Y') for entry in monthly_trend],
        'data': [float(entry['total']) for entry in monthly_trend]
    }
    
    category_chart_data = {
        'labels': [entry['category__name'] for entry in category_data],
        'data': [float(entry['total']) for entry in category_data],
        'colors': [entry['category__color'] or '#007bff' for entry in category_data]
    }
    
    context = {
        'stats': stats,
        'category_data': category_data,
        'monthly_trend': monthly_trend,
        'weekly_trend': weekly_trend,
        'top_waste': top_waste,
        'impact': impact,
        'monthly_data': json.dumps(monthly_data),
        'category_chart_data': json.dumps(category_chart_data),
        'filter_form': filter_form
    }
    
    return render(request, 'waste_logs/analytics.html', context)

@login_required
def goals(request):
    """Waste reduction goals list view"""
    # Get all user's goals
    active_goals = WasteGoal.objects.filter(
        user=request.user,
        is_completed=False
    ).order_by('end_date')
    
    completed_goals = WasteGoal.objects.filter(
        user=request.user,
        is_completed=True
    ).order_by('-end_date')
    
    # Create a new goal
    if request.method == 'POST':
        form = WasteGoalForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goal created successfully.')
            return redirect('waste_goals')
    else:
        form = WasteGoalForm(user=request.user)
    
    context = {
        'active_goals': active_goals,
        'completed_goals': completed_goals,
        'form': form
    }
    
    return render(request, 'waste_logs/goals.html', context)

@login_required
def goal_detail(request, goal_id):
    """Detail view for a specific goal with progress tracking"""
    goal = get_object_or_404(WasteGoal, pk=goal_id, user=request.user)
    
    # Get logs related to this goal's category (if specified)
    related_logs = None
    if goal.category:
        if goal.start_date and goal.end_date:
            related_logs = WasteLog.objects.filter(
                user=request.user,
                category=goal.category,
                date_logged__gte=goal.start_date,
                date_logged__lte=goal.end_date
            ).order_by('-date_logged')
        else:
            related_logs = WasteLog.objects.filter(
                user=request.user,
                category=goal.category,
                date_logged__gte=goal.start_date
            ).order_by('-date_logged')
    
    # Update goal progress
    if request.method == 'POST':
        new_quantity = request.POST.get('current_quantity')
        if new_quantity:
            try:
                goal.current_quantity = float(new_quantity)
                if goal.current_quantity >= goal.target_quantity:
                    goal.is_completed = True
                goal.save()
                messages.success(request, 'Goal progress updated.')
            except ValueError:
                messages.error(request, 'Invalid quantity value.')
        
        # Check if this is a "mark as complete" request
        if request.POST.get('mark_complete'):
            goal.is_completed = True
            goal.save()
            messages.success(request, 'Goal marked as completed!')
            return redirect('waste_goals')
    
    context = {
        'goal': goal,
        'related_logs': related_logs,
    }
    
    return render(request, 'waste_logs/goal_detail.html', context)

@login_required
def delete_goal(request, goal_id):
    """Delete a waste reduction goal"""
    goal = get_object_or_404(WasteGoal, pk=goal_id, user=request.user)
    
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted successfully.')
        return redirect('waste_goals')
    
    return render(request, 'waste_logs/delete_goal.html', {'goal': goal})

from django.db.models.functions import TruncDay

@login_required
def export_data(request):
    """Data export view for waste logs"""
    # Date range filter
    filter_form = DateRangeFilterForm(request.GET)
    filters = Q(user=request.user)
    
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('start_date'):
            filters &= Q(date_logged__gte=filter_form.cleaned_data['start_date'])
        if filter_form.cleaned_data.get('end_date'):
            filters &= Q(date_logged__lte=filter_form.cleaned_data['end_date'])
        if filter_form.cleaned_data.get('category'):
            filters &= Q(category=filter_form.cleaned_data['category'])
    
    # Get filtered logs
    logs = WasteLog.objects.filter(filters).order_by('-date_logged')
    
    context = {
        'logs': logs,
        'filter_form': filter_form,
        'export_types': [
            {'format': 'csv', 'name': 'CSV'},
            {'format': 'json', 'name': 'JSON'},
        ]
    }
    
    return render(request, 'waste_logs/export_data.html', context)


