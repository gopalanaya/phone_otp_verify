from django.urls import path, include
#from . import views

from rest_framework.routers import DefaultRouter
from accounts.api import VoicegateCustomViewSet


default_router = DefaultRouter(trailing_slash=False)

default_router.register('phone', VoicegateCustomViewSet, basename="phone")

urlpatterns = default_router.urls


#urlpatterns = [
#    path("user/", include('rest_framework.urls')),
#    path("totp/create", views.TOTPCreateView.as_view(), name="totp-create"),
#    path("totp/login/<int:token>/", views.TOTPVerifyView.as_view(), name="totp-login"),
#]
