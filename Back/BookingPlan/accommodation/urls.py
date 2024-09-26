from django.urls import path
from . import views

urlpatterns = [
    path('rep_login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('accommodations/<int:pk>/', views.accommodation_detail, name='accommodation_detail'),
    path('recep_accommodations/', views.list_accommodations, name='list_accommodations'),
    path('my_accommodations/', views.receptionist_accommodations, name='receptionist_accommodations'),
    path('my_accommodations/<int:pk>/', views.receptionist_accommodation_detail, name='receptionist_accommodation_detail'),
]