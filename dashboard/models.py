from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Notes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    description=models.TextField()
    def __str__(self):
        return self.title

class Homework(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=50)
    chapter=models.CharField(max_length=70)
    topic=models.TextField()
    due=models.DateTimeField()
    is_finished=models.BooleanField(default=False)

class Todo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    is_finished=models.BooleanField(default=False)

    def __str__(self):
        return self.title