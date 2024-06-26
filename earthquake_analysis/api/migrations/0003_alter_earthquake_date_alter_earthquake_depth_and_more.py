# Generated by Django 5.0.3 on 2024-04-28 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_earthquake_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earthquake',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='depth',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='event_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='magnitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='mb',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='md',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='ml',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='ms',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='mw',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='earthquake',
            name='origin_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
