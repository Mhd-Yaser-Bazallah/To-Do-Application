from django.db import models
from django.contrib.auth.hashers import make_password


class CustomUser(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=25)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES,default='client')
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=128,null=False)  

    def set_password(self, raw_password):
          self.password = make_password(raw_password)

    def __str__(self):
        return self.email      