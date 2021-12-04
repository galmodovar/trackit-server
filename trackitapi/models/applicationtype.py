from django.db import models
from trackitapi.models.type import JobType
from trackitapi.models.application import Application

class ApplicationType(models.Model):
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)