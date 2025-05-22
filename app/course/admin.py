from django.contrib import admin
from .models import Course, Bob, Lesson, UserProgress, Bookmark, Note

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    ordering = ['order']

@admin.register(Bob)
class BobAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_active', 'created_at']
    list_filter = ['course', 'is_active', 'created_at']
    search_fields = ['title', 'course__title']
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'bob', 'order', 'estimated_reading_time', 'is_active', 'created_at']
    list_filter = ['bob__course', 'bob', 'is_active', 'created_at']
    search_fields = ['title', 'body', 'bob__title']

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'is_completed', 'completion_date', 'time_spent']
    list_filter = ['is_completed', 'completion_date', 'lesson__bob__course']
    search_fields = ['user__username', 'lesson__title']

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'created_at']
    list_filter = ['created_at', 'lesson__bob__course']
    search_fields = ['user__username', 'lesson__title']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'created_at', 'updated_at']
    list_filter = ['created_at', 'lesson__bob__course']
    search_fields = ['user__username', 'lesson__title', 'content']