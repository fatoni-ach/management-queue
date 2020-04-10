from django.shortcuts import render

def index(request):
    context = {
        'judul':'Home'
    }
    return render(request, 'index.html', context)

def login(request):
    context = {
        'title':'Login Page'
    }
    return render(request, "login.html", context)