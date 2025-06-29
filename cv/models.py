from django.db import models

# Create your models here.
from django.db import models

class Yetenek(models.Model):
    ad = models.CharField(max_length=100)

    def __str__(self):
        return self.ad

class Deneyim(models.Model):
    pozisyon = models.CharField(max_length=100)
    sirket = models.CharField(max_length=100)
    aciklama = models.TextField()
    baslangic = models.DateField()
    bitis = models.DateField(blank=True, null=True)
    saim= models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.pozisyon} - {self.sirket}"

from django.db import models

class Hesap(models.Model):
    kod = models.CharField(max_length=20, unique=True)
    ad = models.CharField(max_length=100)
    tur = models.CharField(max_length=10, choices=[('A', 'Aktif'), ('P', 'Pasif')])
    ust_hesap = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.kod} - {self.ad}"

class Fis(models.Model):
    tarih = models.DateField()
    aciklama = models.CharField(max_length=255, blank=True)
    belge_no = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.tarih} - {self.aciklama}"

class FisHareket(models.Model):
    fis = models.ForeignKey(Fis, related_name='hareketler', on_delete=models.CASCADE)
    hesap = models.ForeignKey(Hesap, on_delete=models.PROTECT)
    aciklama = models.CharField(max_length=255, blank=True)
    borc = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    alacak = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.hesap} | Borç: {self.borc} | Alacak: {self.alacak}"