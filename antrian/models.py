from django.db import models
import datetime
from django.utils import dateformat

# Create your models here.
class DataPasien(models.Model):
    GENDER = (
        ('l', 'L'),
        ('p', 'P'),
        )
    DARAH = (
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
         ('O', 'O'),
        ) 
    nama_pasien     = models.CharField(max_length=191, blank=False)
    no_ktp          = models.CharField(max_length=20, blank=False)
    jenis_kelamin   = models.CharField(max_length=1, blank=False, choices=GENDER, default='l')
    tempat_tgl_lahir= models.CharField(max_length=191, blank=True)
    Status          = models.CharField(max_length=191, blank=False)
    gol_darah       = models.CharField(max_length=2, choices=DARAH, blank=True, default='A')
    no_telp         = models.CharField(max_length=12, blank=False)
    alamat          = models.CharField(max_length=191, blank=False)
    created_at      = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at       = models.DateTimeField(auto_now=True, blank=True)
    
    def __str__(self):
        return "{}.{}:{}".format(self.id, self.nama_pasien, self.no_telp)

class NoAntrian(models.Model):
    no              = models.IntegerField(default=0)
    durasi          = models.IntegerField(default=0)
    data_pasien     = models.ForeignKey(DataPasien, on_delete=models.CASCADE, default=1)
    status          = models.CharField(max_length=9, blank=True)
    pemanggil       = models.CharField(max_length=20, blank=True)
    jenis_pengobatan= models.CharField(max_length=20, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at      = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return "id={} |no={} |durasi{} |status = {} |pasien={}".format(
            self.id, self.no, self.durasi, self.status, self.data_pasien.nama_pasien)

class Pasien(models.Model):
    GENDER = (
        ('l', 'Laki-laki'),
        ('p', 'Perempuan'),
        )
    no_antrian      = models.ForeignKey(NoAntrian,null=True, blank=True, on_delete=models.CASCADE)
    nama_pasien     = models.CharField(max_length=191, blank=True)
    jenis_kelamin   = models.CharField(choices=GENDER, max_length=10, default='l')
    umur            = models.IntegerField(blank=True)
    nama_dokter     = models.CharField(max_length=191, blank=True)
    jenis_pengobatan= models.CharField(max_length=191)
    waktu_mulai     = models.CharField(max_length=191, blank=True)
    waktu_berakhir  = models.CharField(max_length=191, blank=True)
    durasi_pengobatan= models.IntegerField(blank=True, null=True, default=0)
    created_at      = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at       = models.DateTimeField(auto_now=True, blank=True)

    # def save(self):
    #     self.waktu_mulai = dateformat.format(datetime.datetime.now() , 'H:i:s')
    #     super(Pasien, self).save()

    def __str__(self):
        return "{}.{}".format(self.id, self.nama_pasien)