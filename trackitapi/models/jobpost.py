from django.db import models


class JobPost(models.Model):
    company = models.CharField(max_length=50)
    company_url = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    role_url = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    