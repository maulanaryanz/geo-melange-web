from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profil/', views.profile_view, name='profil'),
    path('portofolio/', views.portofolio_view, name='portofolio'),
    path('kontak/', views.contact_view, name='kontak'),
]