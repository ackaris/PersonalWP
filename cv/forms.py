from django import forms
from .models import Hesap
from django.forms import inlineformset_factory
from .models import Fis, FisHareket
class HesapForm(forms.ModelForm):
    class Meta:
        model = Hesap
        fields = ['kod', 'ad', 'tur', 'ust_hesap']
        widgets = {
            'kod': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'örnek: 100.01',
                'oninput': "this.value = this.value.toUpperCase();"
            }),
            'ad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'örnek: Kasa Hesabı'
            }),
            'tur': forms.Select(attrs={'class': 'form-select'}),
            'ust_hesap': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'kod': 'Tekil hesap kodu (örn. 100, 120.01)',
            'ust_hesap': 'Varsa bu hesabın bağlı olduğu üst hesap',
        }

class FisForm(forms.ModelForm):
    class Meta:
        model = Fis
        fields = ['tarih', 'aciklama', 'belge_no']
        widgets = {
            'tarih': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'aciklama': forms.TextInput(attrs={'class': 'form-control'}),
            'belge_no': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formset: Aynı fişe ait birden çok hareket eklemek için
FisHareketFormSet = inlineformset_factory(
    Fis,
    FisHareket,
    fields=['hesap', 'aciklama', 'borc', 'alacak'],
    extra=2,  # Varsayılan olarak 2 boş satır gelsin
    widgets={
        'hesap': forms.Select(attrs={'class': 'form-select'}),
        'aciklama': forms.TextInput(attrs={'class': 'form-control'}),
        'borc': forms.NumberInput(attrs={'class': 'form-control'}),
        'alacak': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)