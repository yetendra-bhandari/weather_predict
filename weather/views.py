from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from weather.models import User


def home(request):
    message = request.session.pop('message', None)
    return render(request, 'weather/index.html', {'message': message})


def register(request):
    return HttpResponse("You're at the registration page.")


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
