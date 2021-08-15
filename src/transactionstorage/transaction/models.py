from django.db import models
from transactionstorage.client.models import Client
from django.utils.timezone import now

TRANSACTION_TYPES = ('in', 'out')


class Transaction(models.Model):
    type = models.CharField(choices=zip(TRANSACTION_TYPES, TRANSACTION_TYPES), null=False, max_length=3)
    amount = models.IntegerField(null=False, blank=False, default=0)
    datetime = models.DateTimeField(null=False, default=now)

    client = models.ForeignKey(Client, null=False, blank=False, on_delete=models.PROTECT, related_name="transactions")

    class Meta:
        indexes = (
            (models.Index(fields=['datetime'])),
        )
