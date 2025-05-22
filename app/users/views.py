from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, 'template/page/login.html')

def register_view(request):
    return render(request, 'template/page/register.html')