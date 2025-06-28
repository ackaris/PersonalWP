from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hesaplar/', views.hesap_listesi, name='hesap_listesi'),
    path('fis-ekle/', views.fis_ekle, name='fis_ekle'),
]