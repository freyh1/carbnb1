from dj_rest_auth.serializers import (
    PasswordResetSerializer as BasePasswordResetSerializer,
)
from django.conf import settings
from rest_framework import serializers

from api.models import User, Car, Booking, CarImage, Review, Location
from api.utils import password_reset_url_generator


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        exclude = ['user_permissions', 'is_superuser', 'last_login', 'date_joined']
        read_only_fields = ['username', 'is_staff', 'is_active', 'groups']

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        if obj.image and obj.image.url:
            ret['image'] = obj.image.url
        return ret


class ContactFormSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
    message = serializers.CharField(required=True, allow_blank=False, max_length=200)


class PasswordResetSerializer(BasePasswordResetSerializer):
    """
    Override to redirect to our frontend using a custom password_reset_url_generator.
    """

    def save(self):
        from allauth.account.forms import default_token_generator

        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'token_generator': default_token_generator,
            'url_generator': password_reset_url_generator,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"
        read_only_fields = ["owner"]

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ["id", "username"]
        

class ReviewSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["user", "car", "created_at"]


class CarDetailSerializer(serializers.ModelSerializer):
    owner = PublicUserSerializer(read_only = True)
    location = serializers.StringRelatedField()
    images = serializers.StringRelatedField(many=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
            model = Car
            fields = "__all__"

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ["id", "image"]

class CarListSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    location = serializers.StringRelatedField()

    class Meta:
        model = Car
        fields = ["id", "make", "model", "price_per_day", "is_available", "images", "location"]


class BookingSerializer(serializers.ModelSerializer):
    car = CarListSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["user", "car", "total_price", "created_at", "is_confirmed"]



class LocationSerializer(serializers.Serializer):
    class Meta:
        model = Location
        fields = "__all__"
