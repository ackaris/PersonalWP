from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hesaplar/', views.hesap_listesi, name='hesap_listesi'),
    path('fis-ekle/', views.fis_ekle, name='fis_ekle'),
    path('fisler/', views.fis_listesi, name='fis_listesi'),
    path('fis/<int:fis_id>/sil/', views.fis_sil, name='fis_sil'),
    path('fis/<int:fis_id>/duzenle/', views.fis_duzenle, name='fis_duzenle'),
    path('fis/<int:fis_id>/', views.fis_detay, name='fis_detay'),
    path('muhasebe/', views.muhasebe_panel, name='muhasebe_panel'),
    path('hesap/<int:hesap_id>/duzenle/', views.hesap_duzenle, name='hesap_duzenle'),
    path('hesap/<int:hesap_id>/sil/', views.hesap_sil, name='hesap_sil'),
]