from django.db import models
from user.models import User

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    create_date = models.DateField(auto_now=True)
    due_date = models.DateField()

    def __str__(self):
        return self.name

class BoardUser(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)

