from django.db import models
from viewflow.models import Process


class WorkflowProcess(Process):
    text = models.CharField(max_length=150)
    approved = models.BooleanField(default=False)

