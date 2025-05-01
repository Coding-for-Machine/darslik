from django.urls import path
from .views import home, lesson


urlpatterns = [
    path("", home),
    path("dars/", lesson),
]
