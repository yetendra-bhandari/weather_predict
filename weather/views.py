import io
import csv

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError

from .models import User
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
        csv = request.FILES['data']
        if csv.name.endswith('.csv'):
            processCSV(csv)
        else:
            request.session['message'] = 'Please Upload A CSV File'
    except(AssertionError, ZeroDivisionError):
        pass
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
    except(AssertionError, IntegrityError):
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
    except(AssertionError, User.DoesNotExist):
        request.session['message'] = 'Invalid Email Or Password'
        return HttpResponseRedirect(reverse('home'))


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('home'))
