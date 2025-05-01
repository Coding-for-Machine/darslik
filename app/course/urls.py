from django.urls import path
from .views import home, lesson


urlpatterns = [
    path("", home, name="home"),
    path("<slug:slug>/", lesson, name='lesson'),
]
