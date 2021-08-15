# Generated by Django 3.2.6 on 2021-08-15 14:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('in', 'in'), ('out', 'out')], max_length=3)),
                ('amount', models.IntegerField(default=0)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='client.client')),
            ],
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['type'], name='transaction_type_923941_idx'),
        ),
    ]
