from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('assessor', 'Assessor'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def is_student(self):
        return self.role == 'student'

    def is_assessor(self):
        return self.role == 'assessor'
