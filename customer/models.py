from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name
