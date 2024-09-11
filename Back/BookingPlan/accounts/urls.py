from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('', views.home_view, name='home'),
    path('destination/', views.dashboard_view, name='destination'),
    path('agency/', views.agency_view, name='agency'),
    path('stays/', views.stays_view, name='stays'),
    path('schedule/', views.stays_view, name='schedule'),
    path('tips/', views.tips_view, name='tips'),
    path('base/', views.base_view, name='base'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_profile/', views.create_profile, name='create_profile'),

]
