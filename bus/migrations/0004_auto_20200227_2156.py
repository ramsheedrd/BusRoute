# Generated by Django 2.0.3 on 2020-02-27 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0003_auto_20200227_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routemodel',
            name='stand_delay',
        ),
        migrations.AddField(
            model_name='tripmodel',
            name='stand_delay',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
