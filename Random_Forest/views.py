from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from antrian.models import NoAntrian, Pasien, DataPasien
from django.utils.formats import dateformat
import datetime
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
import csv

def index(request):
    context = {
        'title':'Home',
        'body_judul':'No antrian',
    }
    id = str(request.user)
    if request.method == "POST":
        noantrian = NoAntrian.objects.get(id = request.POST['no_sekarang'])
        if noantrian.status == "uncall":
            noantrian.status = "call"
            noantrian.pemanggil = id
            setDataSet(noantrian)

        elif noantrian.status == "call":
            noantrian.status = "called"
            setWaktuBerakhir(noantrian)
        noantrian.save()
        return redirect('index')
    if request.user.is_authenticated():
        antrian = NoAntrian.objects.all().exclude(status="called").order_by('no')
        # antrian = NoAntrian.objects.all()
        antrian_cek = antrian.filter(pemanggil = request.user)
        if antrian_cek.exists() : 
            no_sekarang = antrian_cek[0]
            antrian = antrian.exclude(no = no_sekarang.no)
        elif antrian.exists() :
            no_sekarang = antrian[0]
            antrian = antrian.exclude(no = no_sekarang.no)
        else : 
            no_sekarang = {
                'no':0,
                'status':''
            }
        context.update({
            'antrian':antrian,
            'no_sekarang':no_sekarang,
        })
        return render(request, "index.html", context)
    else :
        return redirect('login')

def reset(request):
    antrian = NoAntrian.objects.all()
    for data in antrian : 
        data.status = "uncall"
        data.pemanggil = ""
        data.save()
    return redirect('index')

def login_view(request):
    context = {
        'title':'Login Page'
    }
    if request.user.is_authenticated():
        return redirect('antrian:index')
    if request.method == "POST":
        username_input = request.POST['username']
        password_input = request.POST['password']
        user = authenticate(request, username = username_input, password = password_input)
        if user is not None :
            login(request, user)
            return redirect('index')
        else :
            messages.error(request, 'Username atau password tidak valid')
            return redirect('login')
    return render(request, "login.html", context)

def poli(request, jenis_pengobatan):
    context = {
        'title':'Home',
        'body_judul':'No antrian',
    }
    id = str(request.user)
    if request.method == "POST":
        noantrian = NoAntrian.objects.get(id = request.POST['no_sekarang'])
        if noantrian.status == "uncall":
            noantrian.status = "call"
            noantrian.pemanggil = id
            setDataSet(noantrian)

        elif noantrian.status == "call":
            noantrian.status = "called"
            setWaktuBerakhir(noantrian)
        noantrian.save()
        poli = '/poli/'+jenis_pengobatan
        return redirect(poli)
    if request.user.is_authenticated():
        antrian1 = NoAntrian.objects.all().exclude(status="called").order_by('no')
        # antrian = NoAntrian.objects.all()
        jenis_pengobatan_input = getJenisPengobatan(jenis_pengobatan)
        antrian = antrian1.filter(jenis_pengobatan = jenis_pengobatan_input)
        antrian_cek = antrian.filter(pemanggil = request.user)
        if antrian_cek.exists() : 
            no_sekarang = antrian_cek[0]
            antrian = antrian.exclude(no = no_sekarang.no)
        elif antrian.exists() :
            no_sekarang = antrian[0]
            antrian = antrian.exclude(no = no_sekarang.no)
        else : 
            no_sekarang = {
                'no':0,
                'status':''
            }
        context.update({
            'antrian':antrian,
            'no_sekarang':no_sekarang,
            'jenis_pengobatan': jenis_pengobatan_input,
        })
        return render(request, "index.html", context)
    else :
        return redirect('login')

def data_antrian(request):
    noantrian = NoAntrian.objects.all().order_by('-created_at')
    context = {
        'title':'Data Antrian',
        'body_judul':'Data Antrian',
        'no_antrian':noantrian,
    }
    return render(request, "pasien.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def setDataSet(noAntrian):
    from api.views import getAge
    dataPasien  = DataPasien.objects.get(id = noAntrian.data_pasien.id)
    umur        = getAge(dataPasien.tempat_tgl_lahir)
    nama_dokter = getNamaDokter(noAntrian.jenis_pengobatan)
    data = {
        'nama_pasien'       : noAntrian.data_pasien.nama_pasien,
        'jenis_kelamin'     : noAntrian.data_pasien.jenis_kelamin,
        'umur'              : umur,
        'nama_dokter'       : nama_dokter,
        'jenis_pengobatan'  : noAntrian.jenis_pengobatan,
        'waktu_mulai'       : dateformat.format(datetime.datetime.now(), 'H:i:s'),
        'waktu_berakhir'    : "",
        'durasi_pengobatan' : 0, 
        'no_antrian'        : noAntrian,
    }
    Pasien.objects.bulk_create([Pasien(**data)])

def download_data(request):
    noantrian = NoAntrian.objects.all().order_by('-created_at')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="data_antrian.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'no_antrian','nama_pasien', 'status','poli', 'durasi'])
    users = NoAntrian.objects.all().values_list('id','no','data_pasien', 'status', 'jenis_pengobatan', 'durasi')
    for user in users:
        writer.writerow(user)
        print(user)
    return response

def getNamaDokter(jenis_pengobatan):
    if jenis_pengobatan == "Penyakit dalam":
        return "Dr Wahyu H"
    elif jenis_pengobatan == "spesialis saraf":
        return "Dr Eny S"
    elif jenis_pengobatan == "klinik bedah":
        return "m lutfi"

def setWaktuBerakhir(noAntrian):
    pasien_update = Pasien.objects.get(no_antrian=noAntrian, waktu_berakhir="")
    pasien_update.waktu_berakhir = dateformat.format(datetime.datetime.now() , 'H:i:s')
    time1 = datetime.datetime.strptime(pasien_update.waktu_mulai, '%H:%M:%S')
    time2 = datetime.datetime.strptime(pasien_update.waktu_berakhir, '%H:%M:%S')
    durasi = time2-time1
    d = int(durasi.total_seconds())
    pasien_update.durasi_pengobatan = d
    print(pasien_update)
    pasien_update.save()

def getJenisPengobatan(jenis_pengobatan):
    if jenis_pengobatan=="klinik_bedah":
        return "klinik bedah"
    elif jenis_pengobatan=="spesialis_saraf":
        return "spesialis saraf"
    elif jenis_pengobatan=="penyakit_dalam":
        return "Penyakit dalam"