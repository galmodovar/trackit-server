from django.db import models
from django.contrib.auth.models import User

class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=50)