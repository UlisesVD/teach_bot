from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_CHOICES = (
        ('student', 'Alumno'),
        ('teacher', 'Maestro')
    )
    type = models.CharField(
        max_length=7,
        choices=USER_CHOICES,
        default='student',
    )
    # add additional fields in here

    def __str__(self):
        return self.email