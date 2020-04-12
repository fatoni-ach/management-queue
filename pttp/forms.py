from django import forms
from antrian.models import Pasien

class TestingForms(forms.ModelForm):
    class Meta():
        model       = Pasien
        fields      = [
            'nama_pasien',
            'jenis_kelamin',
            'umur',
            'nama_dokter',
            'jenis_pengobatan',
        ]

        labels  = {
            'nama_pasien' : 'Nama Pasien',
            'jenis_kelamin' : 'Jenis Kelamin',
            'umur' : 'Umur',
            'nama_dokter': 'Nama Dokter',
            'jenis_pengobatan' : 'Poli',
        }

        DOKTER = Pasien.objects.all().values_list("nama_dokter","nama_dokter").distinct()
        POLI = Pasien.objects.all().values_list("jenis_pengobatan","jenis_pengobatan").distinct()
        
        widgets = {
             'nama_pasien': forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'Nama',
                }
            ),
            'jenis_kelamin': forms.Select(
                attrs={
                    'class':'custom-select custom-select-sm form-control form-control-sm',
                },
                
            ),
            'umur': forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'Umur',
                }
            ),
            'nama_dokter': forms.Select(
                choices = DOKTER,
                attrs={
                    'class':'custom-select custom-select-sm form-control form-control-sm',
                }
            ),
            'jenis_pengobatan': forms.Select(
                choices = POLI,
                attrs={
                    'class':'custom-select custom-select-sm form-control form-control-sm',
                }
            ),
        }


class TempForms(forms.Form):
    year    = forms.IntegerField(required = False
    )
    month    = forms.IntegerField(required = False
    )
    day    = forms.IntegerField(required = False
    )
    week    = forms.CharField(required = False,
        max_length=20,
    )
    temp_2    = forms.IntegerField(required = False
    )
    temp_1    = forms.IntegerField(required = False
    )
    average    = forms.FloatField(required = False
    )
    actual    = forms.IntegerField(required = False
    )
    forecast_noaa    = forms.IntegerField(required = False
    )
    forecast_acc    = forms.IntegerField(required = False
    )
    forecast_under    = forms.IntegerField(required = False
    )
    csv      = forms.FileField()
