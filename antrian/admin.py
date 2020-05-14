from django.contrib import admin

# Register your models here.

from .models import Pasien, DataPasien, NoAntrian

admin.site.register(Pasien)
admin.site.register(DataPasien)
admin.site.register(NoAntrian)