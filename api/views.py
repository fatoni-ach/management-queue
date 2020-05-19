from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
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
        dataPasien = DataPasien.objects.get(no_telp=no_telp_data)
        data = {
            'no':4,
            'durasi':15,
            'data_pasien':dataPasien,
            'status':'uncall',
            'pemanggil':'',
        }
        NoAntrian.objects.bulk_create([NoAntrian(**data)])
        noAntrian = NoAntrian.objects.get(data_pasien=dataPasien, status="uncall")
        noAntrian1 = noAntrianSerializers(instance=data)
        return JsonResponse(noAntrian1.data, safe=False)

@api_view(['POST'])
def getStatus(request):
    if request.method == "POST":
        if request.POST["action"] == "umum":
            noAntrian = NoAntrian.objects.filter(status="uncall").order_by('-created_at')
            no = noAntrian[0].no+1
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
            noAntrian = NoAntrian.objects.filter(status="uncall").order_by('created_at')
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

