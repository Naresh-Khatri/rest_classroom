from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserProfile:
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)


class CalenderEvent(models.Model):
    creater = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True)
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255, default='')
    color = models.CharField(max_length=10, default='orange')


    def __str__(self):
        return f'{self.date} - {self.title}'
    

class Meeting(models.Model):
    last_updated = models.DateField(auto_now_add=True)
    date = models.DateField()
    starting_at = models.TimeField()
    ending_at = models.TimeField()
    subject = models.CharField(max_length=100)
    creater = models.ForeignKey(User, default=1, related_name='creater', on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, related_name='instructor', on_delete=models.CASCADE)
    topic = models.CharField(max_length=100, null=True)
    link = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.instructor} - {self.subject}'