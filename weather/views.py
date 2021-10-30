from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Data
from .utils import processCSV, getProbability


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
    return render(request, 'weather/app.html', {'message': message, 'name': request.session['name'], 'datalist': Data.objects.all()})


def upload(request):
    try:
        assert request.method == 'POST'
        data = request.FILES['data']
        if data.name.endswith('.csv'):
            p = processCSV(data)

            chi2_square = p['chi2_score']
            p.pop('chi2_score', None)
            request.session['message'] = 'Chi Square Values: ' + \
                str(chi2_square[0]) + '\n, p-values: ' + str(chi2_square[1])

            Data.objects.create(
                csvname=request.session['name'] + "_" + data.name, **p)
        else:
            request.session['message'] = 'Please Upload A CSV File'
    except Exception:
        request.session['message'] = 'Invalid CSV File'
    finally:
        return HttpResponseRedirect(reverse('app'))


def predict(request):
    try:
        data_id, features, outlook, temp, humidity, windy = request.GET['data'], request.GET['features'], request.GET[
            'outlook'], request.GET['temp'], request.GET['humidity'], request.GET['windy']
        data = Data.objects.get(id=data_id)
        good, bad = getProbability(
            data, features, outlook, temp, humidity, windy)
        request.session['message'] = 'Good Weather Probability => ' + str(good) + '%, Bad Weather Probability => ' + str(
            bad) + '%, Prediction => ' + ('Good' if(good > bad) else 'Bad') + ' Weather.'
    except Exception as e:
        print(e)
        request.session['message'] = 'Invalid Data Provided'
    finally:
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
    except Exception:
        request.session['message'] = 'Email Address Already Exists'
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
        if (type(e) == User.DoesNotExist):
            request.session['message'] = 'Email Address Does Not Exist'
        else:
            request.session['message'] = 'Incorrect Password'
        return HttpResponseRedirect(reverse('home'))


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('home'))
