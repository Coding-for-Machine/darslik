from django.db import models
from django.urls import reverse
# Create your models here.

# 7 sinif darstlik
 
class Course(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to="course/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("lesson", args=[str(self.slug)])
    


class Bob(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    icone = models.CharField(max_length=250, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="bob")
    def __str__(self):
        return self.title
    
    
