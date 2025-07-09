from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='waste_logs_home'),  # alias for base.html
    path('report/', views.report, name='waste_report'),
]
