from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Create your views here.
def index(request):
    if request.method == "POST":
        if request.POST['action'] == "cek_id":
            context = {
                'status':'ada',
                'no_antrian':15,
            }
            return JsonResponse(context)
    context = {
        'title':'api'
    }
    context1 = {
        "error": "0",
        "message": "Successfull",
        "prediction": "Normal",
        "confidence_score": 69.0,
        'status':'tidakada'
    }
    return JsonResponse(context1)