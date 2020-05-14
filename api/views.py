from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Create your views here.
def index(request):
    context = {
        'title':'api'
    }
    context1 = {
        "error": "0",
        "message": "Successfull",
        "prediction": "Normal",
        "confidence_score": 69.0
    }
    return JsonResponse(context1)