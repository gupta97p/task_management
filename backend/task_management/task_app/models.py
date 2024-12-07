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
