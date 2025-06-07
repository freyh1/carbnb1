from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework import mixins, viewsets, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.models import User, Car
from api.permissions import UserPermission
from api.serializers import ContactFormSerializer, UserSerializer, CarSerializer, CarDetailSerializer, CarListSerializer



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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def mine(self, request):
        cars = self.queryset.all()  #filter(owner=request.user)
        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return CarDetailSerializer
        elif self.action in ["mine", "list"]:
            return CarListSerializer
        return CarSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
