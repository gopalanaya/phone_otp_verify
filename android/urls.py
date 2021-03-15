from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name="subscribe"),
    path('verify_mobile/<str:token>', views.verify_phone, name="verify_phone"),
    path('success', views.success_page, name="success"),

]
