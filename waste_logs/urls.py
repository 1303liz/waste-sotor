from django.urls import path
from . import views
from debug_view import debug_subcategories

urlpatterns = [
    path('', views.index, name='waste_logs_home'),
    path('report/', views.report, name='waste_report'),
    path('analytics/', views.analytics, name='waste_analytics'),
    path('goals/', views.goals, name='waste_goals'),
    path('export/', views.export_data, name='waste_export'),
    path('debug-subcategories/', debug_subcategories, name='debug_subcategories'),
    
    # Waste log CRUD
    path('log/<int:log_id>/', views.waste_log_detail, name='waste_log_detail'),
    path('log/<int:log_id>/edit/', views.edit_waste_log, name='edit_waste_log'),
    path('log/<int:log_id>/delete/', views.delete_waste_log, name='delete_waste_log'),
    path('log/<int:log_id>/add-entry/', views.add_waste_entry, name='add_waste_entry'),
    
    # Goal management
    path('goal/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('goal/<int:goal_id>/delete/', views.delete_goal, name='delete_goal'),
    
    # AJAX endpoints
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
]
