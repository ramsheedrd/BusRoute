# Generated by Django 2.0.3 on 2020-03-14 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0010_rentbusmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placesmodel',
            name='district',
        ),
        migrations.AlterField(
            model_name='rentbusmodel',
            name='ac',
            field=models.BooleanField(default=False),
        ),
    ]
