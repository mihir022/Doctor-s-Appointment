from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *


# Create your views here.
def Home(request):
    doctor = Doctor.objects.all()
    con = {
        'doctor':doctor
    }
    return render(request, 'home.html', con)

def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not password1 == password2:
            messages.info(request, 'Password Not match')
        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already found')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already found')
            return redirect('register')
            
        usr = User(username=username, email=email)
        usr.set_password(password1)
        usr.save()

    return render(request, 'register.html')

def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'Username not found')

        usr = authenticate(username=username, password=password)
        if usr is None:
            messages.info(request, 'Invalid Password')
            return redirect('login')

        login(request, usr)
        return redirect('home')

    return render(request, 'login.html')

def LogoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')

def Apoinment(request):
    user = request.user
    ap = Appointment.objects.filter(user=request.user)

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        age = request.POST['age']
        contact = request.POST['contact']
        address = request.POST['address']
        street = request.POST['street']
        city = request.POST['city']
        pincode = request.POST['pincode']
        doctor = request.POST['doctor']

        appointment = Appointment(user=user, firstname=firstname, lastname=lastname, age=age, 
            contact=contact, address=address, street=street, city=city, doctor=doctor, pincode=pincode)
        appointment.save()
        
    return render(request, 'apoinment.html', {'ap':ap})

def UpdateApoinment(request, id):
    if request.method =='POST':
        updt = Appointment.objects.get(pk=id)
        frm = AppointmentForm(request.POST, instance=updt)

        if frm.is_valid():
            frm.save()
    else:
        updt = Appointment.objects.get(pk=id)
        frm = AppointmentForm(instance=updt)
    return render(request, 'update.html', {'frm':frm})

def DeleteApoinment(request, id):
    if request.method == 'POST':
        dlt = Appointment.objects.get(pk=id)
        dlt.delete()
        return redirect('apoinment')