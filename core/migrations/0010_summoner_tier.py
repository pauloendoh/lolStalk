# Generated by Django 2.0.2 on 2018-03-23 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_summoner_summonerid'),
    ]

    operations = [
        migrations.AddField(
            model_name='summoner',
            name='tier',
            field=models.CharField(default='Challenger', max_length=30),
            preserve_default=False,
        ),
    ]
