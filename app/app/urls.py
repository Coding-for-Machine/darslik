from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from course.api import api
from users.urls import urlpatterns as users_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("course.urls")),
    path("api/", api.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("users/", include(users_urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
