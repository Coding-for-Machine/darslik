from django.db import models

# Create your models here.

# 7 sinif darstlik

class Course(models.Model):
    title = models.CharField(max_length=250)
    sulg = models.SlugField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to="course/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


class Bob(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    icone = models.CharField(max_length=250, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
    
