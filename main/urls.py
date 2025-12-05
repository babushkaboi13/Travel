# main/urls.py (файл в приложении main)
from django.urls import path
from . import views

app_name = 'main'  # Это важно!

urlpatterns = [
    path('', views.home, name='home'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('booking/', views.create_booking, name='create_booking'),
    path('payment/', views.create_payment, name='payment'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
]