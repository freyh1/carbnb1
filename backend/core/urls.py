from allauth.account.views import confirm_email
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers

from api.views import (
    BookingViewSet,
    UserViewSet,
    CarViewSet,
    CarImageViewSet,
    ReviewViewSet,
    MyCarListingsView,
    Signup,
    Login,
    LogoutView,
    contact,
)

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("cars", CarViewSet, basename="car")
router.register("bookings", BookingViewSet, basename="booking")
router.register("car-images", CarImageViewSet, basename="car-image")
router.register("reviews", ReviewViewSet, basename="review")

urlpatterns = (
    [
        path("admin/", admin.site.urls),

        # ✅ All API routes under /api/
        path("api/", include(router.urls)),

        # ✅ Auth views
        path("api/signup/", Signup.as_view(), name="api-signup"),
        path("api/login/", Login.as_view(), name="api-login"),
        path("api/logout/", LogoutView.as_view(), name="api-logout"),

        # ✅ Extra API views
        path("api/my-cars/", MyCarListingsView.as_view(), name="api-my-cars"),
        path("api/contact/", contact, name="api-contact"),

        # ✅ Auth packages (dj-rest-auth / allauth)
        path("api/auth/", include("dj_rest_auth.urls")),
        path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
        path("api/accounts/", include("allauth.urls")),

        # ✅ Email confirm
        re_path(
            r"^api/confirm-email/(?P<key>[-:\w]+)/$",
            confirm_email,
            name="account_confirm_email",
        ),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
