# Generated by Django 2.0.2 on 2018-03-24 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_summoner_tier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='summoner_match',
            name='match',
        ),
        migrations.AddField(
            model_name='summoner_match',
            name='gameId',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
