import logging
import random
import string
from datetime import datetime, timedelta, timezone

import names
from django.core.management import BaseCommand

from transactionstorage.user.models import CustomUser
from transactionstorage.storage.models import TRANSACTION_TYPES, Transaction

logger = logging.getLogger(__name__)

NAMES_COUNT = 20000
TRANSACTIONS_PER_NAME = 20
LEN_FOR_BULK_CREATE = 10000

STEP_TIME = timedelta(days=1)
START_DATETIME = datetime(2020, 8, 15, tzinfo=timezone.utc)
END_DATETIME = datetime.now(timezone.utc)


def _random_hash(n=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))


class Command(BaseCommand):
    help = "Script that is executed after restoration of prod db into dev envs"

    def handle(self, *args, **options):

        self.stdout.write("Creating users and transactions")

        transactions = []
        for _ in range(NAMES_COUNT):
            # create not right away, but by 10.000 instances
            if len(transactions) > LEN_FOR_BULK_CREATE:
                Transaction.objects.bulk_create(transactions)
                transactions = []

            first_name, last_name = names.get_full_name().split()
            user = CustomUser.objects.create(
                username=f"{first_name}.{last_name}{_random_hash()}",
                first_name=first_name, last_name=last_name, balance=0.00
            )

            for _ in range(TRANSACTIONS_PER_NAME):
                transaction_datetime = START_DATETIME + random.randrange((END_DATETIME - START_DATETIME)
                                                                         // STEP_TIME + 1) * STEP_TIME

                transaction_type = random.choice(TRANSACTION_TYPES)
                amount_unsigned = random.randint(1, 100)

                transactions.append(
                    Transaction(
                        type=transaction_type,
                        user_id=user.id,
                        amount=amount_unsigned if transaction_type == 'in' else -amount_unsigned,
                        transaction_datetime=transaction_datetime
                    )
                )
        self.stdout.write("Users and transactions created successfully")