# Generated by Django 5.1.3 on 2024-11-26 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_history_stop_history_end_history_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='distance',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='history',
            name='end_loc_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='start_loc_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]