# Generated by Django 3.2.9 on 2021-11-30 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountapp', '0010_auto_20211130_0346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moneytransfer',
            old_name='send_from',
            new_name='from_account',
        ),
        migrations.RenameField(
            model_name='moneytransfer',
            old_name='send_to',
            new_name='from_to',
        ),
        migrations.RenameField(
            model_name='moneytransfer',
            old_name='transection_date',
            new_name='transaction_date',
        ),
        migrations.AlterField(
            model_name='userbankaccount',
            name='account_no',
            field=models.PositiveIntegerField(default='9147108607', unique=True),
        ),
    ]