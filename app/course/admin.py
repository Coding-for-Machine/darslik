from django.contrib import admin
from .models import Course, Bob
# Register your models here.


class CouserAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug", "body", "created_at", "updated_at"]
admin.site.register(Course, CouserAdmin)


admin.site.register(Bob)