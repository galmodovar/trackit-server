from django.db import models

class Status(models.Model):
    status = models.CharField(max_length=50)