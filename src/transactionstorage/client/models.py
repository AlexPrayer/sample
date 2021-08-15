from django.db import models


class Client(models.Model):  # I don't want to mix django's default user with this instance
    first_name = models.CharField(null=False, blank=False, max_length=255)
    last_name = models.CharField(null=False, blank=False, max_length=255)
