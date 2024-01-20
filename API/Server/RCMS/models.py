from django.db import models
from django.contrib.auth.models import AbstractUser

#Model to store user credentals
class RegisteredUsers(AbstractUser) :
    name = models.CharField(max_length=255)
    email=models.EmailField(max_length=255,unique=True)
    password=models.CharField(max_length=255,unique=True)

    #By default Django uses username to login , But we will use 'email' field to login
    username=None
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS =[]

    


