# Generated by Django 2.0.2 on 2018-03-31 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20180328_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summoner_match',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
