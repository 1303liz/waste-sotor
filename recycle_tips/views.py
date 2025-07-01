from django.shortcuts import render
from django.http import HttpResponse

def tips_home(request):
    return render(request, 'recycle_tips/tips_home.html')

def tip_detail(request):
    return render(request, 'recycle_tips/tips_detail.html')





