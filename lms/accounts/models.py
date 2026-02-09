from django.db import models

class SignupUser(models.Model):
    full_name = models.CharField(max_length=100)
    
    email      = models.EmailField(unique=True)
    phone      = models.CharField(max_length=15, blank=True, null=True)
    
    username   = models.CharField(max_length=100, unique=True)
    password   = models.CharField(max_length=255)  # hashed

    def __str__(self):
        return self.username


class LoginRecord(models.Model):
    user = models.OneToOneField(SignupUser, on_delete=models.CASCADE)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
