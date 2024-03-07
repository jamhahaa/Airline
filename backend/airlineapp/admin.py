# Register your models here.
from django.contrib import admin
from .models import Flight, City, Reservation, Admin, Passenger

admin.site.register(Flight)
admin.site.register(City)
admin.site.register(Reservation)
admin.site.register(Passenger)
admin.site.register(Admin)
