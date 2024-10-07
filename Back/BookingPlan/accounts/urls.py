from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('base/', views.base_view, name='base'),    
    path('', views.home_view, name='home'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_profile/', views.create_profile, name='create_profile'),


    path('admin_home/', views.admin_home_view, name='admin_home'),
    path('create_receptionist/', views.create_receptionist_view, name='create_receptionist'),
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('edit_user/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('create_agency/', views.create_agency_view, name='create_agency'),
    path('agencies/', views.list_agencies_view, name='list_agencies'),
    path('agency/update/<int:agency_id>/', views.update_agency_view, name='update_agency'),
    path('agency/delete/<int:agency_id>/', views.delete_agency_view, name='delete_agency'),


    path('agency_login/', views.login, name='agency_login'),
    path('agency_home/', views.agency_home_view, name='agency_home'),
    path('my-agency/', views.agency_receptionist, name='agency_receptionist'),
    path('listagencies/', views.list_agencies, name='list_agency'),



    path('destination/', views.dashboard_view, name='destination'),
    path('destination_list/', views.destination_list, name='destination_list'),
    path('destination_detail/', views.destination_detail, name='doualaStays'),

    path('accommodations/', views.accommodation_list, name='accommodation_list'),
    path('accommodation/<int:pk>/', views.accommodation_detail, name='accommodation_detail'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:pk>/eticket/', views.generate_eticket, name='generate_eticket'),
    


    path('stays/', views.stays_view, name='stays'),
    path('schedule/', views.stays_view, name='schedule'),
    path('tips/', views.tips_view, name='tips'),

]
