from django.db import models as m
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

ALPHANUMERIC = "abcdefghjkmnpqrstuvwxyz01234567889"

# Create your models here.
class Account(m.Model):
    user = m.OneToOneField(User, on_delete=m.CASCADE, related_name="profile")
    is_teacher = m.BooleanField(default=False)
    is_student = m.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"

class Responder(m.Model):
    work = m.FileField(blank=True)
    student = m.ForeignKey(Account, on_delete=m.CASCADE, related_name="responder")
    score = m.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)], blank=True)

    def __str__(self):
        return f"{self.student.user.username}"

class Assignment(m.Model):
    title = m.CharField(max_length=69)
    description = m.CharField(max_length=640)
    code = m.CharField(default=User.objects.make_random_password(length=6, allowed_chars=ALPHANUMERIC), max_length=6)
    teacher = m.ManyToManyField(Account, related_name="grader")
    # students = m.ManyToManyField(Account, related_name="responders", blank=True)
    # responses = m.ManyToManyField(Response, related_name="answers", blank=True)
    responders = m.ManyToManyField(Responder, related_name="volunteer", blank=True)

    def __str__(self):
        return f"{self.title} | code -> {self.code}"
