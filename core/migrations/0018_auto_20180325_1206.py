# Generated by Django 2.0.2 on 2018-03-25 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_champions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Champions',
            new_name='Champion',
        ),
    ]