from allauth.account.views import confirm_email
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers

from api.views import (
    BookingViewSet,
    UserViewSet,
    CarViewSet,
    CarImageViewSet,
    home,
    my_bookings,
    profile,
    signup,
    login,
    logout,
    my_car_listings,
    create_car,
    car_detail,
    book_car,
    contact,
)

router = routers.DefaultRouter()

router.register(r"users", UserViewSet, basename="user")
router.register("cars", CarViewSet, basename="car")
router.register("bookings", BookingViewSet, basename="booking")
router.register("car-images", CarImageViewSet, basename="car-image")

urlpatterns = (
    [
        path('', home, name='home'),
        path('signup/', signup, name='signup'),
        path('login/', login, name='login'),
        path('logout/', logout, name='logout'),
        path('admin/', admin.site.urls),
        path('api/', include(router.urls)),
        path('api/contact/', contact),
        path('my-cars', my_car_listings, name='my_car_listings'),
        path('create-car', create_car, name='create_car'),
        path('cars/<int:car_id>/', car_detail, name='car_detail'),
        path('cars/<int:car_id>/book/', book_car, name='book_car'),
        path('my-bookings/', my_bookings, name='my_bookings'),
        path('profile/', profile, name='profile'),

        # Path used to build our password reset link.
        # path(
        #     "password-reset/confirm/<uidb64>/<token>/",
        #     TemplateView.as_view(template_name="password_reset_confirm.html"),
        #     name='password_reset_confirm'
        # ),

        path('api/auth/', include("dj_rest_auth.urls")),
        path(
            'api/auth/registration/',
            include('dj_rest_auth.registration.urls')
        ),


        path(
            'api/accounts/',
            include('allauth.urls'),
            name='socialaccount_signup'
        ),

        # Address our adapter will build to give a link to our frontend.
        # See api.adapter.AccountAdapter.
        re_path(
            r"^confirm-email/(?P<key>[-:\w]+)/$",
            confirm_email,
            name="account_confirm_email",
        ),

    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")

)
