from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name_ar = models.CharField("الاسم بالعربي", max_length=150, blank=True)
    name_en = models.CharField("Name (EN)", max_length=150, blank=True)

    def __str__(self):
        return self.username
