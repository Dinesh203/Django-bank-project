# Generated by Django 3.2.9 on 2021-11-29 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountapp', '0007_auto_20211129_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbankaccount',
            name='contact',
            field=models.IntegerField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='userbankaccount',
            name='account_no',
            field=models.PositiveIntegerField(default='9245807035', unique=True),
        ),
    ]