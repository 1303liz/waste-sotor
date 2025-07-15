from django.urls import path
from . import views

urlpatterns = [
    path('', views.tips_home, name='tips_home'),  
    path('detail/', views.tip_detail, name='tip_detail'),
    path('detail/<int:tip_id>/', views.tip_detail, name='tip_detail_id'),
    path('add/', views.add_tip, name='add_tip'),
    path('category/<str:category>/', views.category_tips, name='category_tips'),
]

