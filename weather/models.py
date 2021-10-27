from django.db import models


class User(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.email
