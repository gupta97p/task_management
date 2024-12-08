from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.contrib.auth.models import UserManager



class userReg(AbstractUser):
    
    GENDER_CHOICE = [('Male', 'Male'),('Female', 'Female')]
    
    username = models.CharField(max_length=20, unique=True, blank=False)
    mobile = models.CharField(max_length=10, blank=True, null=True, unique=True)
    age = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    gender = models.CharField(max_length=8,choices=GENDER_CHOICE,  default='Male')

    objects = UserManager()

    def __str__(self):
        return self.username


class Task(models.Model):
    TASK_STATUS = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(userReg, on_delete=models.CASCADE, related_name='users_tasks')
    task_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=TASK_STATUS, default='Pending')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name


