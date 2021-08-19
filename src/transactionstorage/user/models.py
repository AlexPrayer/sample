from django.contrib.auth.models import AbstractUser
from django.db import models

TRANSACTION_TYPES = ('in', 'out')


class CustomUser(AbstractUser):
    balance = models.DecimalField(decimal_places=2, max_digits=15)

    class Meta:
        db_table = 'user'
