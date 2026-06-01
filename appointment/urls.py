from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),

    path('login/', views.login_user, name='login'),

    path('logout/', views.logout_user, name='logout'),

    path('home/', views.home, name='home'),

    path('patients/', views.patients, name='patients'),

    path('edit/<int:id>/', views.edit_patient, name='edit'),

    path('delete/<int:id>/', views.delete_patient, name='delete'),

    path('export/', views.export_csv, name='export'),

    path('book/', views.public_booking, name='book'),

    path('success/', views.success, name='success'),
    
    path('Thank You/', views.thank_you, name='Thank You'),

]