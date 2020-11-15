from django.db import models as m


class Airport(m.Model):
    code = m.CharField(max_length=3)
    city = m.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} {self.code}"

# Create your models here.
class Flight(m.Model):
    origin = m.ForeignKey(Airport, on_delete=m.CASCADE, related_name="departures")
    destination = m.ForeignKey(Airport, on_delete=m.CASCADE, related_name="arrivals")
    duration = m.IntegerField()

    def __str__(self):
        return f"{self.id} - {self.origin} to {self.destination}"

class Passenger(m.Model):
    first = m.CharField(max_length=100)
    last = m.CharField(max_length=100)
    flights = m.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"
