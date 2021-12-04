from django.db import models
from trackitapi.models.applicant import Applicant
from trackitapi.models.status import Status 
from trackitapi.models.stage import Stage
from trackitapi.models.jobpost import JobPost




class Application(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    notes = models.TextField()
    response = models.BooleanField()
    date_applied = models.DateField()
    skills = models.ManyToManyField("Type", through="ApplicationType", related_name="skills")
    
    