# Generated by Django 3.2.6 on 2021-08-19 14:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('in', 'in'), ('out', 'out')], max_length=3)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('transaction_datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]