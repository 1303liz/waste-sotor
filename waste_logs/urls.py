from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='waste_home'),
    path('report/', views.report, name='waste_report'),
]
