from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import WasteLog
from .forms import WasteLogForm

@login_required
def index(request):
    logs = WasteLog.objects.filter(user=request.user).order_by('-date_logged')
    return render(request, 'waste_logs/home.html', {'logs': logs})

@login_required
def report(request):
    if request.method == 'POST':
        form = WasteLogForm(request.POST)
        if form.is_valid():
            waste_log = form.save(commit=False)
            waste_log.user = request.user
            waste_log.save()
            return redirect('waste_logs_home')
    else:
        form = WasteLogForm()
    return render(request, 'waste_logs/report.html', {'form': form})


