# Generated by Django 2.0.2 on 2018-03-23 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='summoner',
            name='region',
            field=models.CharField(default='', max_length=5),
            preserve_default=False,
        ),
    ]
