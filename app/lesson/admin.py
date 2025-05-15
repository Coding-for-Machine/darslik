from django.contrib import admin

# Register your models here.
from .models import Lessons
from django.db import models
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }

admin.site.register(Lessons, ArticleAdmin)