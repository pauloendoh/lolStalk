# Generated by Django 2.0.2 on 2018-03-31 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_summoner_match_summoner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='summoner_match',
            name='summoner',
        ),
    ]
