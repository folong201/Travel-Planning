from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('base/', views.base_view, name='base'),    
    path('', views.home_view, name='home'),
    path('destination/', views.dashboard_view, name='destination'),
    path('destination_list/', views.destination_list, name='destination_list'),
    path('destination_detail/', views.destination_detail, name='doualaStays'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_profile/', views.create_profile, name='create_profile'),

    path('accommodations/', views.accommodation_list, name='accommodation_list'),
    path('accommodation/<int:pk>/', views.accommodation_detail, name='accommodation_detail'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:pk>/eticket/', views.generate_eticket, name='generate_eticket'),
    
    path('agencies/', views.agencies_list, name='agencies_list'),


    path('stays/', views.stays_view, name='stays'),
    path('schedule/', views.stays_view, name='schedule'),
    path('tips/', views.tips_view, name='tips'),

]
