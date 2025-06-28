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

class Hesap(models.Model):
    TUR_SECENEKLERI = [
        ('aktif', 'Aktif'),
        ('pasif', 'Pasif'),
        ('gelir', 'Gelir'),
        ('gider', 'Gider'),
        ('nazim', 'Nazım'),
    ]

    kod = models.CharField(max_length=20, unique=True)
    ad = models.CharField(max_length=200)
    tur = models.CharField(max_length=10, choices=TUR_SECENEKLERI)
    ust_hesap = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Muhasebe Hesabı"
        verbose_name_plural = "Muhasebe Hesapları"

    def __str__(self):
        return f"{self.kod} - {self.ad}"
class Fis(models.Model):
    tarih = models.DateField()
    aciklama = models.CharField(max_length=255)
    belge_no = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.tarih} - {self.aciklama}"


class FisHareket(models.Model):
    fis = models.ForeignKey(Fis, on_delete=models.CASCADE, related_name='hareketler')
    hesap = models.ForeignKey(Hesap, on_delete=models.CASCADE)
    aciklama = models.CharField(max_length=255, blank=True)
    borc = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    alacak = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.hesap.kod} - Borç: {self.borc} / Alacak: {self.alacak}"