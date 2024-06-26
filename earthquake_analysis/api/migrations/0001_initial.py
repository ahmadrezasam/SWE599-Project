# Generated by Django 5.0.3 on 2024-03-15 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Earthquake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('origin_time', models.TimeField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('depth', models.FloatField()),
                ('magnitude', models.FloatField()),
                ('md', models.FloatField()),
                ('ml', models.FloatField()),
                ('mw', models.FloatField()),
                ('ms', models.FloatField()),
                ('mb', models.FloatField()),
                ('event_type', models.CharField(max_length=10)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
    ]
