from rest_framework import permissions

from api.models import User


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user: User = request.user
        return user.is_authenticated and user.is_active

    def has_object_permission(self, request, view, user_object):
        user: User = request.user
        if user.is_authenticated and user.is_active:
            if request.method in permissions.SAFE_METHODS:
                return True
            if user.is_superuser or user == user_object:
                return True
        return False


class CarPermission(permissions.BasePermission):
    """Only allow owners or superusers to modify cars."""

    def has_object_permission(self, request, view, car):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_superuser or car.owner == request.user
        )


class BookingPermission(permissions.BasePermission):
    """Restrict updates and deletes to the booking user or car owner."""

    def has_object_permission(self, request, view, booking):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user.is_superuser
            or booking.user == request.user
            or booking.car.owner == request.user
        )
    

class CarImagePermission(permissions.BasePermission):
    """Only allow owners or superusers to modify car images."""

    def has_object_permission(self, request, view, car_image):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_superuser or car_image.car.owner == request.user
        )


class ReviewPermission(permissions.BasePermission):
    """Only allow authors or superusers to modify reviews."""

    def has_object_permission(self, request, view, review):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_superuser or review.user == request.user
        )
