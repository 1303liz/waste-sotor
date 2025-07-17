from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Tip
from .forms import TipForm

def tips_home(request):
    # Get filter parameters from GET request
    category = request.GET.get('category', None)
    content_type = request.GET.get('type', None)
    
    # Start with all tips
    tips = Tip.objects.all()
    
    # Apply filters if provided
    if category:
        tips = tips.filter(category=category)
    
    if content_type == 'visual':
        tips = tips.filter(is_visual_guide=True)
    elif content_type == 'practice':
        tips = tips.filter(is_best_practice=True)
    elif content_type == 'tutorial':
        tips = tips.filter(is_tutorial=True)
    
    # Get counts for sidebar
    category_counts = {
        'recyclables': Tip.objects.filter(category='recyclables').count(),
        'compostables': Tip.objects.filter(category='compostables').count(),
        'general_waste': Tip.objects.filter(category='general_waste').count(),
        'plastic': Tip.objects.filter(category='plastic').count(),
        'organic': Tip.objects.filter(category='organic').count(),
        'e_waste': Tip.objects.filter(category='e-waste').count(),
        'general': Tip.objects.filter(category='general').count(),
    }
    
    type_counts = {
        'visual': Tip.objects.filter(is_visual_guide=True).count(),
        'practice': Tip.objects.filter(is_best_practice=True).count(),
        'tutorial': Tip.objects.filter(is_tutorial=True).count(),
    }
    
    # Prepare context
    context = {
        'tips': tips.order_by('-date_posted'),
        'category_counts': category_counts,
        'type_counts': type_counts,
        'selected_category': category,
        'selected_type': content_type,
        'section_info': {
            'title': 'Recycle Tips Section',
            'purpose': 'Provide a learning area for facilitators to educate members on proper waste sorting.',
            'target_audience': 'Facilitators and community members',
            'goal': 'Improve understanding and execution of effective waste separation practices.'
        }
    }
    
    return render(request, 'recycle_tips/tips_home.html', context)

@login_required
def tip_detail(request, tip_id=None):
    if tip_id:
        tip = get_object_or_404(Tip, id=tip_id)
    else:
        # If no specific tip is requested, get the latest
        tip = Tip.objects.order_by('-date_posted').first()
        if not tip:
            messages.info(request, "No tips available yet. Why not add the first one?")
            return redirect('add_tip')
    
    # Get related tips (same category)
    related_tips = Tip.objects.filter(category=tip.category).exclude(id=tip.id)[:3]
    
    context = {
        'tip': tip,
        'related_tips': related_tips,
        'section_info': {
            'title': 'Recycle Tips Section',
            'purpose': 'Provide a learning area for facilitators to educate members on proper waste sorting.',
            'target_audience': 'Facilitators and community members',
            'goal': 'Improve understanding and execution of effective waste separation practices.'
        }
    }
    
    return render(request, 'recycle_tips/tip_detail.html', context)

@login_required
def add_tip(request):
    if request.method == 'POST':
        form = TipForm(request.POST, request.FILES)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.author = request.user
            tip.save()
            messages.success(request, "Your recycling tip has been added successfully!")
            return redirect('tip_detail_id', tip_id=tip.id)
    else:
        form = TipForm()
    
    context = {
        'form': form,
        'section_info': {
            'title': 'Add New Recycling Tip',
            'purpose': 'Share your knowledge to help educate the community about proper waste sorting.',
            'target_audience': 'Facilitators and community members',
            'goal': 'Contribute to our collection of waste management resources.'
        }
    }
    
    return render(request, 'recycle_tips/add_tip.html', context)

@login_required
def category_tips(request, category):
    """View to show tips filtered by category"""
    tips = Tip.objects.filter(category=category)
    
    context = {
        'tips': tips,
        'category': category,
        'category_display': dict(Tip._meta.get_field('category').choices).get(category, category.title()),
        'section_info': {
            'title': f'{category.title()} Recycling Tips',
            'purpose': 'Learn specific techniques for this waste category.',
            'target_audience': 'Facilitators and community members',
            'goal': 'Master the proper handling of this specific waste type.'
        }
    }
    
    return render(request, 'recycle_tips/category_tips.html', context)





