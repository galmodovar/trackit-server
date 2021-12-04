from django.db import models

class JobType(models.Model):
    job_type = models.CharField(max_length=50)