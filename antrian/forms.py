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

        labels  = {
            'nama_pasien' : 'Nama Pasien',
            'jenis_kelamin' : 'Jenis Kelamin',
            'umur'          : 'Umur',
            'nama_dokter'   : 'Nama Dokter',
            'jenis_pengobatan' : 'Poli',
            'waktu_mulai'   : False,
            'waktu_berakhir' : False,
            'durasi_pengobatan' : False,
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
                    # 'class':'form-control form-control-user',
                    'class':'custom-select custom-select-sm form-control form-control-sm',
                }
            ),
            'jenis_pengobatan': forms.Select(
                choices = POLI,
                attrs={
                    'class':'custom-select custom-select-sm form-control form-control-sm',
                    'placeholder':'Poli',
                }
            ),
            'waktu_mulai'       : forms.HiddenInput(),
            'waktu_berakhir'    : forms.HiddenInput(),
            'durasi_pengobatan' : forms.HiddenInput(),
        }
    

class PasienUpdateForms(forms.ModelForm):
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

        labels  = {
            'nama_pasien' : 'Nama Pasien',
            'jenis_kelamin' : 'Jenis Kelamin',
            'umur'          : 'Umur',
            'nama_dokter'   : 'Nama Dokter',
            'jenis_pengobatan' : 'Poli',
            'waktu_mulai'   : 'Waktu Mulai',
            'waktu_berakhir' : 'Waktu Berakhir',
            'durasi_pengobatan' : 'Durasi Pengobatan',
        }
        
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
            'nama_dokter': forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'Nama Dokter',
                }
            ),
            'jenis_pengobatan': forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'Poli',
                }
            ),
            'waktu_mulai'       : forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'Waktu Mulai',
                }
            ),
            'waktu_berakhir'    : forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'Waktu Berakhir',
                }
            ),
            'durasi_pengobatan' : forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'Durasi Pengobatan',
                }
            ),
        }

