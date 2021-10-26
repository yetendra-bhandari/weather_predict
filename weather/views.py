from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from weather.models import User


def home(request):
    message = request.session.pop('message', None)
    return render(request, 'weather/index.html', {'message': message})

def app(request):
    message = request.session.pop('message', None)
    return render(request, 'weather/app.html', {'message': message})


def upload(request):
    return HttpResponseRedirect(reverse('app'))

def predict(request):
    return HttpResponseRedirect(reverse('app'))

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['message'] = 'Invalid Data entered!'
        else:
            request.session['message'] = 'Successfull! Login using same credentials'
    return HttpResponseRedirect(reverse('home'))


def login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
        print(user)
    except(User.DoesNotExist):
        request.session['message'] = 'Invalid Email Or Password'
    finally:
        return HttpResponseRedirect(reverse('home'))


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('home'))
