from django.urls import path
from .views import attendance_form

urlpatterns = [
    path("", attendance_form, name="attendance_form"),
]
