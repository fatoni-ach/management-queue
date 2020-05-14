from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from antrian.models import NoAntrian

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
        elif noantrian.status == "call":
            noantrian.status = "called"
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
            return redirect('login')
    return render(request, "login.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
