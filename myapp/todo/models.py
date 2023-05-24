from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Task(models.Model):
    user = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now().strftime("%Y-%m-%d %H:%M"))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        