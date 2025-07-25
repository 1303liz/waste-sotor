from django.urls import path
from . import views

urlpatterns = [
    path('', views.tips_home, name='tips_home'),  
    path('tip/<int:tip_id>/', views.tip_detail, name='tip_detail'),
    path('add/', views.add_tip, name='add_tip'),
    path('category/<str:category>/', views.category_tips, name='category_tips'),
]

