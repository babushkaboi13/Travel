from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    passport_number = models.CharField(max_length=20)
    birth_date = models.DateField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class Tour(models.Model):
    title = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    duration_days = models.IntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    stars = models.IntegerField()
    description = models.TextField()
    rooms = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Transport(models.Model):
    transport_type = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.transport_type} - {self.company}'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    people = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)



class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50)
    comment = models.CharField(max_length=255)

    def __str__(self):
        return f'Оплата #{self.id}'
