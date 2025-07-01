from django.shortcuts import render
from django.http import HttpResponse



def index(request):
    return render(request, 'waste_logs/home.html')

def report(request):
    return render(request, 'waste_logs/report.html')


