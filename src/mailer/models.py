from django.db import models

# Create your models here.


class ErrorReport(models.Model):
    error = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    issuer = models.CharField(max_length=255)
