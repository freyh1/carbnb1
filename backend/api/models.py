from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


TRANSMISSION_CHOICES = [
    ("manual", "Manual"),
    ("automatic", "Automatic")
]

CAR_TYPE_CHOICES = [
    ("sedan", "Sedan"),
    ("suv", "SUV"),
    ("minivan", "Minivan"),
    ("camper", "Camper"),
    ("hatchback", "Hatchback"),
    ("coupe", "Coupe"),
    ("convertible", "Convertible"),
    ("pickup", "Pickup"),
    ("other", "Other"),
]

FUEL_TYPE_CHOICES = [
    ("petrol", "Petrol"),
    ("diesel", "Diesel"),
    ("hybrid", "Hybrid"),
    ("electric", "Electric"),
]


class Location(models.Model):
    city = models.CharField(max_length=100)
    address = models.TextField()
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address}, {self.city}"


class Car(models.Model):
    description = models.TextField()
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveBigIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars")
    seats = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES, null = True)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, null = True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="car_images/")

    def __str__(self):
        return f"Image for {self.car}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.car} from {self.start_date} to {self.end_date}"


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} ({self.rating}★)"
