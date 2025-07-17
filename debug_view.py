from django.shortcuts import render, redirect
from django.contrib import messages
from waste_logs.models import WasteCategory, WasteSubcategory

def debug_subcategories(request):
    """Debug view to show subcategories"""
    if request.GET.get('action') == 'add_test':
        # Import and run the test subcategories script
        from add_test_subcategories import add_test_subcategories
        try:
            add_test_subcategories()
            messages.success(request, "Test subcategories added successfully!")
        except Exception as e:
            messages.error(request, f"Error adding subcategories: {str(e)}")
        return redirect('debug_subcategories')
    
    categories = WasteCategory.objects.all()
    data = []
    
    for category in categories:
        subcategories = category.subcategories.all()
        data.append({
            'category': category,
            'subcategories': subcategories,
        })
    
    total_subcategories = WasteSubcategory.objects.count()
    
    return render(request, 'debug_subcategories.html', {
        'data': data,
        'total_subcategories': total_subcategories,
    })
