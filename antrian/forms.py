from django import forms
from .models import Pasien

class PasienForms(forms.ModelForm):
    class Meta():
        model       = Pasien
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