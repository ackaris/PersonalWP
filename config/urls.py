from django.contrib import admin
from django.urls import path, include  # include eklenmeli

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cv/', include('cv.urls')),  # cv app'inin urls.py dosyasına yönlendir
]