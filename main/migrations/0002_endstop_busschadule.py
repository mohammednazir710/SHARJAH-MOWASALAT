# Generated by Django 5.0.6 on 2024-11-17 04:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EndStop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_stop', to='main.busstop')),
                ('stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end_stop', to='main.busstop')),
            ],
        ),
        migrations.CreateModel(
            name='BusSchadule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispatch', models.TimeField()),
                ('araival', models.TimeField()),
                ('end_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.endstop')),
            ],
        ),
    ]
