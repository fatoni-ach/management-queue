from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.middleware.csrf import get_token

# Create your views here.
def index(request):
    if(request.method == 'GET' ):
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
            return HttpResponse(context)
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