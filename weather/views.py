from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from weather.models import User


def home(request):
    if 'id' in request.session:
        return HttpResponseRedirect(reverse('app'))
    message = request.session.pop('message', None)
    return render(request, 'weather/index.html', {'message': message})


def app(request):
    message = request.session.pop('message', None)
    return render(request, 'weather/app.html', {'message': message, 'name': request.session['name']})


def upload(request):
    return HttpResponseRedirect(reverse('app'))


def predict(request):
    return HttpResponseRedirect(reverse('app'))


def register(request):
    try:
        user = User.objects.create(
            name=request.POST['name'], email=request.POST['email'].lower(), password=request.POST['password'])
        request.session['id'] = user.id
        request.session['name'] = user.name
        request.session['message'] = 'Registration Successful'
        return HttpResponseRedirect(reverse('app'))
    except:
        request.session['message'] = 'Invalid User Details'
        return HttpResponseRedirect(reverse('home'))


def login(request):
    try:
        user = User.objects.get(email=request.POST['email'].lower())
        assert user.password == request.POST['password']
        request.session['id'] = user.id
        request.session['name'] = user.name
        request.session['message'] = 'Login Successful'
        return HttpResponseRedirect(reverse('app'))
    except:
        request.session['message'] = 'Invalid Email Or Password'
        return HttpResponseRedirect(reverse('home'))


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('home'))
