from django.shortcuts import render, redirect
from django.http import QueryDict
from django.utils import dateformat
from .models import Pasien
from .forms import PasienForms, PasienUpdateForms
import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    context = {
        'title':'dataset antrian',
        'body_judul':'Dataset Antrian Pasien',
    }
    jp      = Pasien.objects.values('jenis_pengobatan').distinct()
    if request.method == "POST" and request.POST['jenis_pengobatan_input'] != 'all':
        jenis_pengobatan_input = request.POST['jenis_pengobatan_input']
        pasien  = Pasien.objects.filter(jenis_pengobatan=jenis_pengobatan_input)
        context.update({
            'jenis_pengobatan_input'    : jenis_pengobatan_input,
        })
    else :
        pasien = Pasien.objects.order_by('-created_at')
        context.update({
            'jenis_pengobatan_input'    : '',
        })
    for pas in pasien:
        pas.durasi_pengobatan = int(pas.durasi_pengobatan/60)
    context.update({
        'pasien':pasien,
        'jp'    : jp
    })
    
    return render(request, 'antrian/index.html', context)

@login_required
def jenis_pengobatan(request):
    jenis_pengobatan_input = request.POST.copy()
    print(jenis_pengobatan_input['jenis_pengobatan_input'])
    # pasien  = Pasien.objects.filter(jenis_pengobatan=jenis_pengobatan_input)
    # jp      = Pasien.objects.value('jenis_pengobatan').distinct()

    context = {
        'title':'dataset antrian',
        'body_judul':'Dataset Antrian',
    #     'pasien':pasien,
    #     'jp'    : jp
    }
    return render(request, 'antrian/index.html', context)


@login_required
def selesai(request, pasien_id):
    pasien_update = Pasien.objects.get(id=pasien_id)
    pasien_update.waktu_berakhir = dateformat.format(datetime.datetime.now() , 'H:i:s')
    time1 = datetime.datetime.strptime(pasien_update.waktu_mulai, '%H:%M:%S')
    time2 = datetime.datetime.strptime(pasien_update.waktu_berakhir, '%H:%M:%S')
    durasi = time2-time1
    d = int(durasi.total_seconds())
    pasien_update.durasi_pengobatan = d
    pasien_update.save()
    return redirect('antrian:index')

@login_required
def create(request):
    pasien_form = PasienForms(request.POST.copy() or None)
    pasien = Pasien.objects.all()
    if request.method == "POST":
        post = request.POST.copy()
        post['waktu_mulai'] = dateformat.format(datetime.datetime.now(), 'H:i:s')
        pasien_form = PasienForms(post)
        if pasien_form.is_valid():
            pasien_form.save()
            return redirect('antrian:index')
    context = {
        'title':'dataset antrian',
        'body_judul':'Dataset Antrian',
        'pasien':pasien,
        'pasien_form':pasien_form,
    }
    return render(request, 'antrian/create.html', context)

@login_required
def update(request, pasien_id):
    pasien_update = Pasien.objects.get(id=pasien_id)
    data = {
        'nama_pasien'       : pasien_update.nama_pasien,
        'jenis_kelamin'     : pasien_update.jenis_kelamin,
        'umur'              : pasien_update.umur,
        'nama_dokter'       : pasien_update.nama_dokter,
        'jenis_pengobatan'  : pasien_update.jenis_pengobatan,
        'waktu_mulai'       : pasien_update.waktu_mulai,
        'waktu_berakhir'    : pasien_update.waktu_berakhir,
    }

    pasien_form = PasienUpdateForms(request.POST or None , initial=data, instance=pasien_update )
    if request.method == "POST" :
        if pasien_form.is_valid():
            pasien_form.save()
            return redirect('antrian:index')

    context = {
        'title':'dataset antrian',
        'body_judul':'Dataset Antrian',
        'pasien_form':pasien_form,
    }

    return render(request, 'antrian/create.html', context)

@login_required
def delete(request, pasien_id):
    Pasien.objects.filter(id=pasien_id).delete()
    return redirect('antrian:index')