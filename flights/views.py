from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
# from the models of this directory only imoprts
from .models import Flight, Passenger
# Create your views here.
def index(request):
    context = {
        "flights" : Flight.objects.all()
    }
    return render(request, "flights/index.html", context)

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight Not found")
    context = dict(
        flight = flight,
        passengers = flight.passengers.all(),
        non_passengers = Passenger.objects.exclude(flights=flight).all()
    )
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return HttpResponse("You dufcjed up")
    except Flight.DoesNotExist:
        return HttpResponse("Bad FLight")
    except Passenger.DoesNotExist:
        return HttpResponse("Basd pick")

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
