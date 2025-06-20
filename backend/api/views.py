from smtplib import SMTPException
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework import mixins, viewsets, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from api.models import User, Car, Booking
from api.permissions import UserPermission, CarPermission, BookingPermission
from api.serializers import (
    ContactFormSerializer,
    UserSerializer,
    CarSerializer,
    CarDetailSerializer,
    CarListSerializer,
    BookingSerializer,
)



@permission_classes([UserPermission])
class UserViewSet(
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user: User = self.request.user

        if self.request.GET.get("me", False):
            return [user]

        return User.objects.all()


@api_view(['POST'])
@permission_classes([AllowAny])
def contact(request):
    serializer = ContactFormSerializer(data=request.data)

    if serializer.is_valid():
        try:
            send_mail(
                subject="Message from a user on NeoTemplate",
                message=f"{serializer.data['email']} vous a écrit:\n\n{serializer.data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except SMTPException:
            return JsonResponse({"error": "An error occured. The message could not be sent."})
    else:
        return JsonResponse(serializer.errors, status=400)

    return JsonResponse({"ok": "ok"})


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def bookings(self, request, pk=None):
        car = self.get_object()

        if car.owner != request.user:
            return Response({"detail": "Not allowed."}, status=403)

        bookings = car.bookings.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "list" and self.request.user.is_authenticated:
            qs = qs.exclude(owner=self.request.user)
        return qs

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, CarPermission]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def book(self, request, pk=None):
        car = self.get_object()
        user = request.user

        if car.owner == user:
            return Response({"detail": "You cannot book your own car."}, status=400)

        start_date_str = request.data.get("start_date")
        end_date_str = request.data.get("end_date")

        if not start_date_str or not end_date_str:
            return Response({"detail": "start_date and end_date are required."}, status=400)

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        if end_date <= start_date:
            return Response({"detail": "End date must be after start date."}, status=400)

        if not car.is_available_during(start_date, end_date):
            return Response({"detail": "Car is not available during this period."}, status=400)

        days = (end_date - start_date).days
        total_price = days * car.price_per_day

        booking = Booking.objects.create(
            user=user,
            car=car,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
        )

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=201)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def mine(self, request):
        cars = self.queryset.filter(owner=request.user)
        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CarDetailSerializer
        elif self.action in ["mine", "list"]:
            return CarListSerializer
        return CarSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['car_type', 'fuel_type', 'transmission', 'seats', 'price_per_day']
    search_fields = ['make', 'model', 'description']
    ordering_fields = ['price_per_day', 'year']


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm(request)
    return render(request, "login.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect("home")

@login_required
def my_car_listings(request):
    return render(request, "my_cars.html")

@login_required
def create_car(request):
    return render(request, "create_car.html")


def car_detail(request, car_id: int):
    return render(request, "car_detail.html", {"car_id": car_id})


@login_required
def book_car(request, car_id: int):
    return render(request, "book_car.html", {"car_id": car_id})

@login_required
def my_bookings(request):
    return render(request, "my_bookings.html")

@login_required
def profile(request):
    return render(request, "profile.html")

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, BookingPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mine(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if booking.car.owner != request.user:
            return Response({"detail": "Not allowed."}, status=403)
        booking.is_confirmed = True
        booking.save()
        return Response({"status": "confirmed"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        booking = self.get_object()
        if booking.car.owner != request.user:
            return Response({"detail": "Not allowed."}, status=403)
        booking.delete()
        return Response({"status": "rejected"})