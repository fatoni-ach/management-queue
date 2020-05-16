from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view

from api.serializers import addSerializers, pasienSerializers, dataPasienSerializers, noAntrianSerializers
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
        return JsonResponse(pasien_serializers.data)
    
    elif request.method == "POST":
        print(request.POST)
        serializers = dataPasienSerializers(data=request.data)
        if serializers.is_valid():
            print(serializers.data)
            return JsonResponse(serializers.data, safe=False)
        else :
            print("GAGAL")
            return JsonResponse("GAGAL", safe=False)

        
