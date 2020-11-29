from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    country = CountryField(blank_label='Select country')
    date_of_birth = models.DateField(blank=True)
    REQUIRED_FIELDS = ['date_of_birth', 'country']
