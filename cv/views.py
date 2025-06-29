from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Hesap, Fis
from .forms import HesapForm, FisForm, FisHareketFormSet

def home(request):
    return render(request, 'cv/home.html')
def fis_listesi(request):
    fisler = Fis.objects.all().order_by('-tarih')
    return render(request, 'cv/fis_listesi.html', {'fisler': fisler})
def fis_detay(request, fis_id):
    fis = get_object_or_404(Fis, id=fis_id)
    hareketler = fis.hareketler.all()
    toplam_borc = sum([h.borc for h in hareketler])
    toplam_alacak = sum([h.alacak for h in hareketler])
    return render(request, 'cv/fis_detay.html', {
        'fis': fis,
        'hareketler': hareketler,
        'toplam_borc': toplam_borc,
        'toplam_alacak': toplam_alacak,
    })
def fis_sil(request, fis_id):
    fis = get_object_or_404(Fis, id=fis_id)
    fis.delete()
    messages.success(request, "Fiş başarıyla silindi.")
    return redirect('fis_listesi')
def hesap_listesi(request):
    hesaplar = Hesap.objects.all().order_by('kod')
    form = HesapForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('hesap_listesi')
    return render(request, 'cv/hesaplar.html', {
        'hesaplar': hesaplar,
        'form': form
    })
def fis_ekle(request):
    form = FisForm(request.POST or None)
    formset = FisHareketFormSet(request.POST or None, prefix='hareket')  # ✅ EKLENDİ

    if request.method == 'POST':
        print("Form valid mi?:", form.is_valid())
        print("Formset valid mi?:", formset.is_valid())
        print("Form errors:", form.errors)
        print("Formset errors:", formset.errors)
        if form.is_valid() and formset.is_valid():
            toplam_borc = toplam_alacak = 0
            for hareket in formset.cleaned_data:
                if not hareket.get('DELETE', False):
                    toplam_borc += hareket.get('borc', 0) or 0
                    toplam_alacak += hareket.get('alacak', 0) or 0

            if toplam_borc != toplam_alacak:
                messages.error(request, "Borç ve alacak eşit değil.")
            else:
                fis = form.save()
                hareketler = formset.save(commit=False)
                for hareket in hareketler:
                    hareket.fis = fis
                    hareket.save()
                formset.save_m2m()
                messages.success(request, "Fiş kaydedildi.")
                return redirect('fis_listesi')
        else:
            messages.error(request, "Form gönderimi başarısız oldu.")

    return render(request, 'cv/fis_ekle.html', {
        'form': form,
        'formset': formset,
        'duzenleme_modu': False,
        'hesaplar': Hesap.objects.all()
    })

def fis_duzenle(request, fis_id):
    fis = get_object_or_404(Fis, id=fis_id)
    form = FisForm(request.POST or None, instance=fis)
    formset = FisHareketFormSet(request.POST or None, instance=fis, prefix='hareket')  # ✅ EKLENDİ

    if request.method == 'POST':
        print("Form valid mi?:", form.is_valid())
        print("Formset valid mi?:", formset.is_valid())
        print("Form errors:", form.errors)
        print("Formset errors:", formset.errors)
        if form.is_valid() and formset.is_valid():
            form.save()
            hareketler = formset.save(commit=False)
            for hareket in hareketler:
                hareket.fis = fis
                hareket.save()
            for silinecek in formset.deleted_objects:
                silinecek.delete()
            messages.success(request, "Fiş başarıyla güncellendi.")
            return redirect('fis_listesi')
        else:
            messages.error(request, "Form gönderimi başarısız oldu. Lütfen alanları kontrol edin.")

    return render(request, 'cv/fis_ekle.html', {
        'form': form,
        'formset': formset,
        'duzenleme_modu': True,
        'hesaplar': Hesap.objects.all()
    })
# cv/views.py
def muhasebe_panel(request):
    return render(request, 'cv/muhasebe_panel.html')

def hesap_duzenle(request, hesap_id):
    hesap = get_object_or_404(Hesap, id=hesap_id)
    form = HesapForm(request.POST or None, instance=hesap)
    if form.is_valid():
        form.save()
        messages.success(request, "Hesap başarıyla güncellendi.")
        return redirect('hesap_listesi')
    return render(request, 'cv/hesap_duzenle.html', {
        'form': form,
        'hesap': hesap
    })

# Yeni: Hesap silme
def hesap_sil(request, hesap_id):
    hesap = get_object_or_404(Hesap, id=hesap_id)

    # Bu hesaba bağlı hareket var mı?
    hareket_sayisi = hesap.fishareket_set.count()
    if hareket_sayisi > 0:
        messages.error(request, f"'{hesap.ad}' hesabına bağlı {hareket_sayisi} hareket olduğu için silinemez.")
        return redirect('hesap_listesi')

    hesap.delete()
    messages.success(request, f"'{hesap.ad}' hesabı başarıyla silindi.")
    return redirect('hesap_listesi')