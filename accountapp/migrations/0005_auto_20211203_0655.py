# Generated by Django 3.2.9 on 2021-12-03 06:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountapp', '0004_auto_20211201_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneytransfer',
            name='deposit_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='userbankaccount',
            name='account_no',
            field=models.PositiveIntegerField(default='9808484910', unique=True),
        ),
        migrations.AlterField(
            model_name='userbankaccount',
            name='contact',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(9999999999), django.core.validators.MinValueValidator(999)]),
        ),
    ]
