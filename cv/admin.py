from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Yetenek, Deneyim

@admin.register(Yetenek)
class YetenekAdmin(admin.ModelAdmin):
    list_display = ('ad',)

@admin.register(Deneyim)
class DeneyimAdmin(admin.ModelAdmin):
    list_display = ('pozisyon', 'sirket', 'baslangic', 'bitis')
    search_fields = ('pozisyon', 'sirket')
    list_filter = ('baslangic',)

from .models import Hesap

@admin.register(Hesap)
class HesapAdmin(admin.ModelAdmin):
    list_display = ('kod', 'ad', 'tur', 'ust_hesap')
    search_fields = ('kod', 'ad')
    list_filter = ('tur',)

from django.contrib import admin
from .models import Hesap, Fis, FisHareket

# Muhasebe Fiş Hareketleri Inline gösterim
class FisHareketInline(admin.TabularInline):
    model = FisHareket
    extra = 1  # Yeni fiş eklerken 1 boş satır varsayılan gelsin

# Muhasebe Fişi Admini
@admin.register(Fis)
class FisAdmin(admin.ModelAdmin):
    list_display = ('tarih', 'aciklama', 'belge_no')
    inlines = [FisHareketInline]  # Satırları fişle birlikte göster

# Alternatif olarak FisHareket'i ayrıca göstermek istersen:
@admin.register(FisHareket)
class FisHareketAdmin(admin.ModelAdmin):
    list_display = ('fis', 'hesap', 'borc', 'alacak')