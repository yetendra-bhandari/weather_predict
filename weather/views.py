from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Data
from .utils import processCSV


def home(request):
    if 'id' in request.session:
        return HttpResponseRedirect(reverse('app'))
    message = request.session.pop('message', None)
    return render(request, 'weather/index.html', {'message': message})


def app(request):
    if 'id' not in request.session:
        request.session['message'] = 'Login Required'
        return HttpResponseRedirect(reverse('home'))
    message = request.session.pop('message', None)
    return render(request, 'weather/app.html', {'message': message, 'name': request.session['name']})


def upload(request):
    try:
        assert request.method == 'POST'
        data = request.FILES['data']
        if data.name.endswith('.csv'):
            p = processCSV(data)
            Data.objects.create(
                user=User.objects.get(id=request.session['id']), csvname=data.name, **p)
        else:
            request.session['message'] = 'Please Upload A CSV File'
    except Exception as e:
        print(e)
    finally:
        return HttpResponseRedirect(reverse('app'))


def predict(request):
    return HttpResponseRedirect(reverse('app'))


def register(request):
    try:
        assert request.method == 'POST'
        user = User.objects.create(
            name=request.POST['name'], email=request.POST['email'].lower(), password=request.POST['password'])
        request.session['id'] = user.id
        request.session['name'] = user.name
        request.session['message'] = 'Registration Successful'
        return HttpResponseRedirect(reverse('app'))
    except Exception as e:
        print(e)
        request.session['message'] = 'Invalid User Details'
        return HttpResponseRedirect(reverse('home'))


def login(request):
    try:
        assert request.method == 'POST'
        user = User.objects.get(email=request.POST['email'].lower())
        assert user.password == request.POST['password']
        request.session['id'] = user.id
        request.session['name'] = user.name
        request.session['message'] = 'Login Successful'
        return HttpResponseRedirect(reverse('app'))
    except Exception as e:
        print(e)
        request.session['message'] = 'Invalid Email Or Password'
        return HttpResponseRedirect(reverse('home'))


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('home'))
