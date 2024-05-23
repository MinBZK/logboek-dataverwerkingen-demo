from django.contrib import admin
from django.urls import path

from munera.views import (
    IndexView,
    LoginView,
    LogoutView,
    ParkingPermitEditlView,
    ParkingPermitListView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("aanmelden", LoginView.as_view(), name="login"),
    path("afmelden", LogoutView.as_view(), name="logout"),
    path("parkeervergunningen", ParkingPermitListView.as_view(), name="parking_permit_list"),
    path("parkeervergunningen/<str:pk>/wijzig", ParkingPermitEditlView.as_view(), name="parking_permit_edit"),
]
