from django.db import models


class JobPost(models.Model):
    company = models.CharField(max_length=50)
    company_url = models.CharField()
    role = models.CharField(max_length=50)
    role_url = models.CharField()
    location = models.CharField(max_length=50)