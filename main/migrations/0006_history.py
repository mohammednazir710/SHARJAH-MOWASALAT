# Generated by Django 5.1.3 on 2024-11-26 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_araival_busschedule_arrival'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.endstop')),
            ],
        ),
    ]