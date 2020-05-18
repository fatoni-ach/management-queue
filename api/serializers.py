from rest_framework import serializers
from rest_framework.serializers import (
	ModelSerializer,
)
from antrian.models import DataPasien, NoAntrian, Pasien

class addSerializers(ModelSerializer):
    class Meta:
        model = DataPasien
        fields = [
            'nama_pasien',
            'no_ktp',
            'jenis_kelamin',
            'tempat_tgl_lahir',
            'Status',
            'gol_darah',
            'no_telp',
            'alamat',
        ]

class pasienSerializers(ModelSerializer):
    class Meta:
        model = Pasien
        fields      = [
            'nama_pasien',
            'jenis_kelamin',
            'umur',
            'nama_dokter',
            'jenis_pengobatan',
            'waktu_mulai',
            'waktu_berakhir',
            'durasi_pengobatan',
        ]


class dataPasienSerializers(ModelSerializer):
    class Meta:
        model = DataPasien
        fields = [
            'nama_pasien',
            'no_ktp',
            'jenis_kelamin',
            'tempat_tgl_lahir',
            'Status',
            'gol_darah',
            'no_telp',
            'alamat',
        ]

class noAntrianSerializers(ModelSerializer):
    data_pasien = dataPasienSerializers()
    class Meta:
        model = NoAntrian()
        fields  = [
            'no',
            'durasi',
            'data_pasien',
            'status',
            'pemanggil',
        ]

class ambilAntrianSerializers(ModelSerializer):
    no_telp         = serializers.CharField(max_length=12)
    jenis_pengobatan= serializers.CharField(max_length=191)