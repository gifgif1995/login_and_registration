from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt
# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pwhash.decode())
        request.session['id'] = user.id
    return redirect('/success')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
    return redirect('/success')

def success(request):
    user = User.objects.get(id=request.session['id']) 
    messages.success(request, "Successfully registered or logged in!")
    return render(request, 'success.html', {'user':user}) 

def logout(request):
    request.session.clear()
    return redirect('/')
