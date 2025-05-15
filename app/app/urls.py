from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from course.api import api
from lesson.api import lesson_router
api.add_router("lesson", lesson_router)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("course.urls")),
    path("api/", api.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
