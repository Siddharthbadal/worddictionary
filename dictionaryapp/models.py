from django.db import models

# Create your models here.

class WordoftheDay(models.Model):
    word=models.CharField(max_length=255)
    definitions=models.TextField()
    timestamp = models.DateTimeField(auto_now=True)