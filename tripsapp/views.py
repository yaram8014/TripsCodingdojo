from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    request.session['action'] = "reg"

    errors = Users.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = Users.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
        
        first_name = user.first_name
        user_id = user.id
        request.session['username'] = first_name
        request.session['id'] = user_id
        return redirect("/trips")

def login(request):
    request.session['action'] = "login"
    errors = Users.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = Users.objects.get(email=request.POST['email'])
        first_name = user.first_name
        user_id = user.id
        request.session['username'] = first_name
        request.session['id'] = user_id
        return redirect('/trips')

def logout(request):
    request.session.flush()
    return redirect('/')


def add_trip(request):
    return render(request, "add_trip.html")

def trips(request):
    if request.session is None:
        return redirect("/")
    else:
        other_trips = Trips.objects.exclude(on_trip = request.session['id'])
        
        context = {
            "other_trips" : other_trips,
            "user" : Users.objects.get(id=request.session['id']), 
        }
        return render(request, "trips.html", context)



def create_trip(request):

    errors = Trips.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/add")
    else:
        dest = request.POST['dest']
        st_date = request.POST['st_date']
        en_date = request.POST['en_date']
        plan = request.POST['plan']

        user = Users.objects.get(id=request.session['id'])
        trip = Trips.objects.create(destnation=dest, start_date=st_date, end_date=en_date, plan=plan , created_by=user)
        creater = Users.objects.get(id=request.session['id'])
        trip.on_trip.add(creater)
        return redirect("/trips")

def remove_trip(request, id):
    trip = Trips.objects.get(id=id)
    trip.delete()
    return redirect("/trips")


def edit(request, id):
    context = {
        "trip" : Trips.objects.get(id=id),
    }
    return render(request, "edit.html", context)

def update(request, id):
    errors = Trips.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/edit/{id}")
    else:
        dest = request.POST['dest']
        st_date = request.POST['st_date']
        en_date = request.POST['en_date']
        plan = request.POST['plan']

        trip = Trips.objects.get(id=id)

        trip.destnation = dest
        trip.start_date = st_date
        trip.end_date = en_date
        trip.plan = plan
        trip.save()
        return redirect("/trips")


def showTrip(request, id):
    context = {
        "trip" : Trips.objects.get(id=id)
    }
    return render(request, "show.html", context)


def join(request, id):
    trip = Trips.objects.get(id=id)
    user = Users.objects.get(id=request.session['id'])
    trip.on_trip.add(user)
    return redirect("/trips")

def cancel(request, id):
    trip = Trips.objects.get(id=id)
    user = Users.objects.get(id=request.session['id'])
    trip.on_trip.remove(user)
    return redirect("/trips")


