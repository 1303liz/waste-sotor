from django.urls import path
from . import views

app_name = 'facilitators'

urlpatterns = [
    path('', views.facilitator_list, name='facilitator_list'),
    path('<int:facilitator_id>/', views.facilitator_detail, name='facilitator_detail'),
    path('processes/', views.recycling_process_list, name='process_list'),
    path('processes/<int:process_id>/', views.recycling_process_detail, name='process_detail'),
    path('impact/', views.recycling_impact, name='impact'),
]
