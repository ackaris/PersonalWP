from django import forms
from .models import Hesap, Fis, FisHareket
from django.forms import inlineformset_factory
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
class HesapForm(forms.ModelForm):
    class Meta:
        model = Hesap
        fields = ['kod', 'ad', 'tur', 'ust_hesap']
        widgets = {
            'kod': forms.TextInput(attrs={'class': 'form-control'}),
            'ad': forms.TextInput(attrs={'class': 'form-control'}),
            'tur': forms.Select(attrs={'class': 'form-select'}),
            'ust_hesap': forms.Select(attrs={'class': 'form-select'}),
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

class FisHareketForm(forms.ModelForm):
    class Meta:
        model = FisHareket
        fields = ['hesap', 'aciklama', 'borc', 'alacak']
        widgets = {
            'hesap': forms.Select(attrs={'class': 'form-select'}),
            'aciklama': forms.TextInput(attrs={'class': 'form-control'}),
            'borc': forms.NumberInput(attrs={'class': 'form-control'}),
            'alacak': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class FisHareketBaseFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        toplam_borc = toplam_alacak = 0

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue

            if not form.cleaned_data:
                continue  # Skip empty forms

            toplam_borc += form.cleaned_data.get('borc') or 0
            toplam_alacak += form.cleaned_data.get('alacak') or 0

        if toplam_borc != toplam_alacak:
            raise forms.ValidationError("Borç ve alacak eşit olmalı.")
# Formset tanımı (prefix burada değil!)
FisHareketFormSet = inlineformset_factory(
    parent_model=Fis,
    model=FisHareket,
    form=FisHareketForm,
    formset=FisHareketBaseFormSet,
    extra=1,
    can_delete=True
)
