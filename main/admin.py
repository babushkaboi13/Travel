from django.contrib import admin
from .models import Client, Tour, Hotel, Transport, Booking, Payment

admin.site.register(Client)
admin.site.register(Tour)
admin.site.register(Hotel)
admin.site.register(Transport)
admin.site.register(Booking)
admin.site.register(Payment)
