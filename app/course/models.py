# courses/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Kurs nomi")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    body = models.TextField(verbose_name="Kurs haqida")
    image = models.ImageField(upload_to='course/', verbose_name="Kurs rasmi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def total_lessons(self):
        return sum(bob.lessons.count() for bob in self.bobs.all())

class Bob(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='bobs')
    title = models.CharField(max_length=200, verbose_name="Bob nomi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Bob"
        verbose_name_plural = "Boblar"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    bob = models.ForeignKey(Bob, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200, verbose_name="Dars nomi", blank=True)
    body = RichTextField(verbose_name="Dars matni")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    estimated_reading_time = models.PositiveIntegerField(default=5, verbose_name="O'qish vaqti (daqiqa)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.bob.title} - Dars {self.order}"
    
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Dars {self.order}"
        super().save(*args, **kwargs)

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    time_spent = models.PositiveIntegerField(default=0, verbose_name="Sarflangan vaqt (soniya)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Foydalanuvchi jarayoni"
        verbose_name_plural = "Foydalanuvchi jarayonlari"
        unique_together = ['user', 'lesson']
    
    def __str__(self):
        return f"{self.user.username} - {self.lesson}"

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Xatcho'p"
        verbose_name_plural = "Xatcho'plar"
        unique_together = ['user', 'lesson']
    
    def __str__(self):
        return f"{self.user.username} - {self.lesson}"

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Eslatma matni")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Eslatma"
        verbose_name_plural = "Eslatmalar"
        unique_together = ['user', 'lesson']
    
    def __str__(self):
        return f"{self.user.username} - {self.lesson} - Eslatma"