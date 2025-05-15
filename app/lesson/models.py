from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from course.models import Bob
# Create your models here.

class Lessons(models.Model):
    bob = models.ForeignKey(Bob, on_delete=models.CASCADE, related_name="lessons")
    body = RichTextUploadingField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.bob.title
    
    
    
