from django.db import models
from section.models import Section
from user.models import User

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now=True)
    due_date = models.DateField()

    def __str__(self):
        return self.name


class TaskUser(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

