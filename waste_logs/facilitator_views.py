from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .facilitator_models import (
    RecyclingFacilitator, RecyclingProcess,
    FacilitatorCollection, RecyclingImpactMetric
)
from django.db.models import Sum, Count

@login_required
def facilitator_list(request):
    """List all active recycling facilitators"""
    facilitators = RecyclingFacilitator.objects.filter(is_active=True).prefetch_related(
        'processes', 'collections', 'impact_metrics'
    )
    
    context = {
        'facilitators': facilitators,
        'page_title': 'Recycling Facilitators'
    }
    
    return render(request, 'waste_logs/facilitators/facilitator_list.html', context)

@login_required
def facilitator_detail(request, facilitator_id):
    """Display detailed information about a specific facilitator"""
    facilitator = get_object_or_404(RecyclingFacilitator, id=facilitator_id, is_active=True)
    
    # Get all processes for this facilitator
    processes = facilitator.processes.all()
    
    # Get collection statistics
    collections = facilitator.collections.all()
    total_collected = collections.aggregate(Sum('quantity_kg'))['quantity_kg__sum'] or 0
    collection_by_category = collections.values('waste_category__name').annotate(
        total=Sum('quantity_kg')
    ).order_by('-total')
    
    # Get impact metrics
    impact_metrics = facilitator.impact_metrics.all()
    
    context = {
        'facilitator': facilitator,
        'processes': processes,
        'collections': collections,
        'total_collected': total_collected,
        'collection_by_category': collection_by_category,
        'impact_metrics': impact_metrics,
        'page_title': facilitator.name
    }
    
    return render(request, 'waste_logs/facilitators/facilitator_detail.html', context)

@login_required
def recycling_process_list(request):
    """List all recycling processes grouped by category"""
    processes = RecyclingProcess.objects.select_related('facilitator', 'waste_category').all()
    
    # Group processes by waste category
    processes_by_category = {}
    for process in processes:
        category = process.waste_category
        if category.name not in processes_by_category:
            processes_by_category[category.name] = {
                'category': category,
                'processes': []
            }
        processes_by_category[category.name]['processes'].append(process)
    
    context = {
        'processes_by_category': processes_by_category,
        'page_title': 'Recycling Processes'
    }
    
    return render(request, 'waste_logs/facilitators/process_list.html', context)

@login_required
def recycling_process_detail(request, process_id):
    """Display detailed information about a specific recycling process"""
    process = get_object_or_404(RecyclingProcess, id=process_id)
    facilitator = process.facilitator
    
    # Get related processes for the same category
    related_processes = RecyclingProcess.objects.filter(
        waste_category=process.waste_category
    ).exclude(id=process_id)[:3]
    
    context = {
        'process': process,
        'facilitator': facilitator,
        'related_processes': related_processes,
        'page_title': process.title
    }
    
    return render(request, 'waste_logs/facilitators/process_detail.html', context)

@login_required
def recycling_impact(request):
    """Display environmental impact metrics from recycling activities"""
    # Get overall impact metrics
    impact_metrics = RecyclingImpactMetric.objects.all().select_related('facilitator')
    
    # Group metrics by type
    metrics_by_type = {}
    for metric in impact_metrics:
        metric_type = metric.get_metric_type_display()
        if metric_type not in metrics_by_type:
            metrics_by_type[metric_type] = []
        metrics_by_type[metric_type].append(metric)
    
    # Get top facilitators by impact
    top_facilitators = RecyclingFacilitator.objects.annotate(
        collection_total=Sum('collections__quantity_kg')
    ).order_by('-collection_total')[:5]
    
    context = {
        'metrics_by_type': metrics_by_type,
        'top_facilitators': top_facilitators,
        'page_title': 'Environmental Impact'
    }
    
    return render(request, 'waste_logs/facilitators/impact.html', context)
