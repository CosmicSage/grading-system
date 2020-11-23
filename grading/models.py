from django.db import models as m
from django.contrib.auth.models import User
# Create your models here.
class Account(m.Model):
    user = m.OneToOneField(User, on_delete=m.CASCADE, related_name="profile")
    is_teacher = m.BooleanField(default=False)
    is_student = m.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"
