from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
import joblib
import datetime
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view

from api.serializers import (
    addSerializers, pasienSerializers, 
    dataPasienSerializers, noAntrianSerializers,
    ambilAntrianSerializers)
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView)
from rest_framework.response import Response
from antrian.models import Pasien, DataPasien, NoAntrian

from rest_framework.permissions import (IsAuthenticated,)
	
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication

PATH_MODEL = "pttp/model/"

# Create your views here.
def index(request):
    if request.method == "GET" :
        token = get_token(request)
        return JsonResponse({'token': token, 'success': 'true'})
    else:
        return JsonResponse({'error': 'true', 'msg': 'Invalid secret'})
    
    if request.method == "POST":
        print(request.POST)
        if request.POST['action'] == "cek_id":
            context = {
                'status':'ada',
                'no_antrian':15,
            }
            return JsonResponse(context)
    # context = {
    #     'title':'api'
    # }
    # context1 = {
    #     "error": "0",
    #     "message": "Successfull",
    #     "prediction": "Normal",
    #     "confidence_score": 69.0,
    #     'status':'tidakada'
    # }
    # return JsonResponse(context1)

class TambahAntrian(ListAPIView):
    serializer_class = addSerializers
    queryset = DataPasien.objects.all()

@api_view(['GET', 'POST'])
def list_pasien(request):
    if request.method == "GET":
        pasien = Pasien.objects.all()
        pasien_serializers = pasienSerializers(pasien, many=True)
        return JsonResponse(pasien_serializers.data, safe=False)
    
    elif request.method == "POST":
        print(request.POST)
        serializer = dataPasienSerializers(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else :
            print("GAGAL")
            return JsonResponse("GAGAL", safe=False)

@api_view(['POST'])
def datapasien(request):
    if request.method == "POST":
        serializer = dataPasienSerializers(data=request.data)
        if serializer.is_valid():
            try:
                dataPasien = DataPasien.objects.get(no_telp = serializer.data["no_telp"])
            except DataPasien.DoesNotExist :
                dataPasien = None
            print(dataPasien)
            if dataPasien != None:
                serializer1 = dataPasienSerializers(instance=dataPasien)
                return JsonResponse(serializer1.data, safe=False)

        print("GAGAL")
        return JsonResponse(serializer.data , safe=False)     

@api_view(['POST'])
def adddatapasien(request):
    if request.method == "POST":
        serializer = dataPasienSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("SUKSES", safe=False)
        else :
            return JsonResponse("GAGAL", safe=False)    

@api_view(['POST'])
def addnoantrian(request):
    if request.method == "POST":
        no_telp_data = request.data["no_telp"]
        jenis_pengobatan_data = request.data["jenis_pengobatan"]
        dataPasien  = DataPasien.objects.get(no_telp=no_telp_data)
        durasi      = getPredict(dataPasien, jenis_pengobatan_data)
        no          = getNoAntrian(jenis_pengobatan_data)
        data = {
            'no'        :no,
            'durasi'    : durasi,
            'data_pasien':dataPasien,
            'status'    :'uncall',
            'pemanggil' :'',
            'jenis_pengobatan':jenis_pengobatan_data,
        }
        NoAntrian.objects.bulk_create([NoAntrian(**data)])
        noAntrian = NoAntrian.objects.get(data_pasien=dataPasien, 
                                        status="uncall", 
                                        jenis_pengobatan=jenis_pengobatan_data)
        noAntrian1 = noAntrianSerializers(instance=data)
        return JsonResponse(noAntrian1.data, safe=False)

@api_view(['POST'])
def getStatus(request):
    if request.method == "POST":
        if request.POST["action"] == "umum":
            jenis_pengobatan = request.POST["jenis_pengobatan"]
            noAntrian = NoAntrian.objects.filter(status="uncall").order_by('-created_at')
            no = getNoAntrian(jenis_pengobatan)
            waktu_tunggu = 0
            for i in noAntrian:
                waktu_tunggu = waktu_tunggu+i.durasi

            hour    = int(waktu_tunggu/60)
            minutes = str(waktu_tunggu%60)
            if hour!= 0 :
                waktu_tunggu_string = str(hour)+" Jam "+minutes+" Menit" 
            else :
                waktu_tunggu_string = minutes+" Menit" 

            data = {
                'no':no,
                'waktu_tunggu':waktu_tunggu_string,
                'jumlah_antrian':noAntrian.count()
            }
            return JsonResponse(data, safe=False)
        elif request.POST["action"] == "private":
            no_telp = request.POST['no_telp']
            status = request.POST['status']
            jenis_pengobatan_input = request.POST['jenis_pengobatan']
            noAntrian = NoAntrian.objects.filter(status="uncall",
                        jenis_pengobatan=jenis_pengobatan_input).order_by('created_at')
            no = 0
            waktu_tunggu = 0
            jumlah_antrian = 0
            status = False
            pasien = ""
            for data in noAntrian:
                if data.data_pasien.no_telp == no_telp:
                    pasien = data.data_pasien.nama_pasien
                    no = data.no
                    status = True
                    break
                else : 
                    waktu_tunggu = waktu_tunggu+data.durasi
                    jumlah_antrian = jumlah_antrian+1
            
            if status==False :
                data = {
                    'no':0,
                    'waktu_tunggu':"null",
                    'jumlah_antrian':0
                }
                return JsonResponse(data , safe=False)
            else:
                hour    = int(waktu_tunggu/60)
                minutes = str(waktu_tunggu%60)
                if hour!= 0 :
                    waktu_tunggu_string = str(hour)+" Jam "+minutes+" Menit" 
                else :
                    waktu_tunggu_string = minutes+" Menit" 
        
                data = {
                    'no':no,
                    'waktu_tunggu':waktu_tunggu_string,
                    'jumlah_antrian':jumlah_antrian
                }
                
                return JsonResponse(data , safe=False)

def getPredict(dataPasien, jenis_pengobatan):
    rfc = joblib.load(PATH_MODEL+"random_forest_model.joblib")
    bins = joblib.load(PATH_MODEL+"bins.joblib")
    time = datetime.datetime.now().time().isoformat(timespec='seconds')
    umur = getAge(dataPasien.tempat_tgl_lahir)
    from Random_Forest.views import getNamaDokter
    nama_dokter = getNamaDokter(jenis_pengobatan)
    a={(dataPasien.jenis_kelamin,
        umur,
        nama_dokter,
        jenis_pengobatan,
        time,
        '10:15:29',
        int(0),
        )} #29
    a = pd.DataFrame(a)
    a.columns = ["jenis_kelamin", "umur", "nama_dokter", "jenis_pengobatan","waktu_mulai", "waktu_berakhir", "durasi_pengobatan"]
    df1 = pd.DataFrame(list(Pasien.objects.all().values_list('jenis_kelamin', 'umur', 'nama_dokter', 'jenis_pengobatan','waktu_mulai', 'waktu_berakhir', 'durasi_pengobatan')))
    df1.columns = ["jenis_kelamin", "umur", "nama_dokter", "jenis_pengobatan","waktu_mulai", "waktu_berakhir", "durasi_pengobatan"]
    temp = df1
    # print(a['waktu_mulai'])
    b = a.append(temp)
    b['waktu_mulai'] = pd.to_datetime(b['waktu_mulai'], format='%H:%M:%S').dt.hour.astype('int64')
    b['umur'] = pd.cut(np.array(b['umur']), [0,12,26,45,100],labels=[0, 1, 2, 3], include_lowest=False).astype('int64')
    # print(b.dtypes)
    categorical_feature_mask = b.dtypes==object
    
    categorical_cols = b.columns[categorical_feature_mask].tolist()
    # print(categorical_cols)
    # b[categorical_cols] = le.fit_transform(b[categorical_cols])
    # print(b[categorical_cols].dtypes)
    le = LabelEncoder()
    b[categorical_cols] = b[categorical_cols].apply(lambda col: le.fit_transform(col.astype(str)))
    b= b.drop('durasi_pengobatan', axis = 1)
    b= b.drop('waktu_berakhir', axis = 1)
    # print(b.dtypes)
    hasil_array = rfc.predict(b.head(1))
    # print(bins[hasil+1])
    hasil = int(bins[hasil_array+1])
    menit = int(hasil/60)
    detik = int(hasil%60)
    return menit

def getAge(date_birthday):
    today = datetime.date.today()
    birthday = datetime.datetime.strptime(date_birthday, "%d-%m-%Y").date()
    if today.month > birthday.month:
        age = int(today.year-birthday.year)
    elif today.month < birthday.month:
        age = int((today.year-birthday.year)-1)
    return age

def getNoAntrian(jenis_pengobatan_input):
    antrian = NoAntrian.objects.all().order_by('-created_at')

    antrian1 = antrian.filter(jenis_pengobatan = jenis_pengobatan_input)

    if antrian1.count() > 0 :
        antrian = antrian1    
    
        for i in antrian:
            print(i.data_pasien)

        tgl_skr = datetime.date.today()
        tgl_db  = timezone.localtime(antrian[0].created_at)
        if tgl_db.date() == tgl_skr:
            no = antrian[0].no+1
        else :
            no = 1
    else:
        no = 1
    return int(no)
