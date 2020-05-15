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
            'created_at',
            'updated_at',
        ]