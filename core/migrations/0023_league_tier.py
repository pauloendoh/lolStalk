# Generated by Django 2.0.2 on 2018-03-28 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_league'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='tier',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
