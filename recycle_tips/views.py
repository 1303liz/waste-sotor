from django.shortcuts import render, get_object_or_404, redirect
from .models import Tip
from .forms import TipForm

def tips_home(request):
    tips = Tip.objects.all().order_by('-date_posted')
    return render(request, 'recycle_tips/tips_home.html', {'tips': tips})

def tip_detail(request, tip_id=None):
    if tip_id:
        tip = get_object_or_404(Tip, id=tip_id)
    else:
        tip = Tip.objects.first()
    return render(request, 'recycle_tips/tips_detail.html', {'tip': tip})

def add_tip(request):
    if request.method == 'POST':
        form = TipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tips_home')
    else:
        form = TipForm()
    return render(request, 'recycle_tips/add_tip.html', {'form': form})





