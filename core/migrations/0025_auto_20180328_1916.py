# Generated by Django 2.0.2 on 2018-03-29 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_summoner_leagues_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summoner',
            name='leagues_updated_at',
            field=models.DateTimeField(),
        ),
    ]
