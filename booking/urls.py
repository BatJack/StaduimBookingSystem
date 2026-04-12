from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('courts/', views.court_list, name='court_list'),
    path('booking/<int:court_id>/', views.booking_form, name='booking_form'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/courts/', views.admin_court_list, name='admin_court_list'),
    path('admin/courts/add/', views.admin_court_add, name='admin_court_add'),
    path('admin/courts/edit/<int:court_id>/', views.admin_court_edit, name='admin_court_edit'),
    path('admin/courts/delete/<int:court_id>/', views.admin_court_delete, name='admin_court_delete'),
    path('admin/availabilities/', views.admin_availability_list, name='admin_availability_list'),
    path('admin/availabilities/add/', views.admin_availability_add, name='admin_availability_add'),
    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin/bookings/add/', views.admin_booking_add, name='admin_booking_add'),
]
