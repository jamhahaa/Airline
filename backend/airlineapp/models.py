from django.db import models
from django.contrib.auth.models import  User


class City(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=100)
    airport_name = models.CharField(max_length=150, default='Mactan-Cebu International Airport')
    airport_code = models.CharField(max_length=10, default='CEB')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name
    
    

class Flight(models.Model):
    TRIP_CHOICES = [
        ('one-way', 'One-Way'),
        ('round-trip', 'Round Trip'),
    ]

    SEAT_TYPE_CHOICES = [
        ('economy', 'Economy Class'),
        ('business', 'Business Class'),
    ]

    flight_number = models.CharField(max_length=10)
    origin = models.ForeignKey(City, related_name='departures', on_delete=models.CASCADE)
    destination = models.ForeignKey(City, related_name='arrivals', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    return_time = models.DateTimeField()
    capacity = models.IntegerField()
    available_seats = models.IntegerField()
    trip_choice = models.CharField(max_length=10, choices=TRIP_CHOICES, default='one-way')
    seat_type = models.CharField(max_length=10, choices=SEAT_TYPE_CHOICES, default='economy')
    economy_class_price = models.IntegerField(default=0)
    business_class_price = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.flight_number} - {self.origin.name} to {self.destination.name}'


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=12)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    seat_type = models.CharField(max_length=10, choices=Flight.SEAT_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - Reservation for {self.flight.flight_number}'

class Passenger(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    contact_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.CharField(max_length=255)

    


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_code = models.CharField(max_length=20)


class AuthUser(models.Model):
    password = models.CharField(max_length=20)
    last_login = models.CharField(max_length=100)
    is_superuser = models.CharField(max_length=2)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    is_staff = models.CharField(max_length=2)
    is_active = models.CharField(max_length=2)
    data_joined = models.CharField(max_length=30)