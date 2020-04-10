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
        GENDER = (
        ('L', 'l'),
        ('P', 'p'),
        )
        
        widgets = {
             'nama_pasien': forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'nama',
                }
            ),
            'jenis_kelamin': forms.Select(
                attrs={
                    'class':'custom-select custom-select-sm form-control form-control-sm',
                },
                choices=GENDER,
                
            ),
            'umur': forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'umur',
                }
            ),
            'nama_dokter': forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'nama dokter',
                }
            ),
            'jenis_pengobatan': forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'jenis pengobatan',
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
