from django.db import models
from django.utils.timezone import now

from transactionstorage.user.models import CustomUser

TRANSACTION_TYPES = ('in', 'out')


class Transaction(models.Model):
    type = models.CharField(choices=zip(TRANSACTION_TYPES, TRANSACTION_TYPES), null=False, max_length=3)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_datetime = models.DateTimeField(null=False, default=now)

    user = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.PROTECT, related_name="transactions")

    class Meta:
        indexes = (
            (models.Index(fields=['transaction_datetime', 'user_id', 'type'])),
        )
