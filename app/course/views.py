from django.shortcuts import render
from .models import Course
# Create your views here.

def home(request):
    courses = Course.objects.all()
    return render(request, "index.html", {"courses": courses})


def lesson(request):
    return render(request, "page/sidbar.html", {})