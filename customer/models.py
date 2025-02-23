from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class Customer(AbstractUser):
#     username = models.CharField(max_length=200, unique=True)
#     email = models.EmailField(max_length=200, unique=True)
#     password = models.CharField(max_length=200)
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     phone = models.CharField(max_length=200)
#     address = models.TextField()
#     date_of_birth = models.DateField()

#     def __str__(self):
#         return self.username
    
#     REQUIRED_FIELDS = ['email', 'username', 'password']
    
    
#     class Meta:
#         app_label = 'customer'
