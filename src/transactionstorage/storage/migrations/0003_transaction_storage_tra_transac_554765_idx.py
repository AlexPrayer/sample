# Generated by Django 3.2.6 on 2021-08-19 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_transaction_user'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['transaction_datetime', 'user_id'], name='storage_tra_transac_554765_idx'),
        ),
    ]
