# Generated by Django 2.0.3 on 2020-03-14 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0011_auto_20200314_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placesmodel',
            name='place_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]