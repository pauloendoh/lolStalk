# Generated by Django 2.0.2 on 2018-03-23 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Summoner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountId', models.FloatField()),
                ('name', models.CharField(max_length=18)),
                ('profileIconId', models.IntegerField()),
                ('revisionDate', models.DateTimeField()),
                ('summonerLevel', models.IntegerField()),
            ],
        ),
    ]
