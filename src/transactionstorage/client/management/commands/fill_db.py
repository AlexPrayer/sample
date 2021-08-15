import logging
import random
from datetime import datetime, timedelta, timezone

import names
from django.core.management import BaseCommand

from transactionstorage.client.models import Client
from transactionstorage.transaction.models import (TRANSACTION_TYPES,
                                                   Transaction)

logger = logging.getLogger(__name__)

NAMES_COUNT = 20000
TRANSACTIONS_PER_NAME = 20
LEN_FOR_BULK_CREATE = 10000

STEP_TIME = timedelta(days=1)
START_DATETIME = datetime(2020, 8, 15, tzinfo=timezone.utc)
END_DATETIME = datetime.now(timezone.utc)


class Command(BaseCommand):
    help = "Script that is executed after restoration of prod db into dev envs"

    def handle(self, *args, **options):

        self.stdout.write("Creating users and transactions")

        client_transactions = []
        for _ in range(NAMES_COUNT):
            # create not right away, but by 10.000 instances
            if len(client_transactions) > LEN_FOR_BULK_CREATE:
                Transaction.objects.bulk_create(client_transactions)
                client_transactions = []

            first_name, last_name = names.get_full_name().split()
            client = Client.objects.create(first_name=first_name, last_name=last_name)

            for _ in range(TRANSACTIONS_PER_NAME):
                date = START_DATETIME + random.randrange((END_DATETIME - START_DATETIME) // STEP_TIME + 1) * STEP_TIME
                client_transactions.append(
                    Transaction(
                        type=random.choice(TRANSACTION_TYPES), client_id=client.id,
                        amount=random.randint(1, 100), datetime=date
                    )
                )
        self.stdout.write("Users and transactions created successfully")
