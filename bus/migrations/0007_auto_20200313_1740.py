# Generated by Django 2.0.3 on 2020-03-13 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0006_hospitalmodel_policestationmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='NearMeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('police', 'Police'), ('hospital', 'Hospital'), ('workshop', 'Workshop')], default='hospital', max_length=20)),
                ('name', models.CharField(max_length=60)),
                ('hospital_category', models.CharField(choices=[('general', 'General Hospital'), ('government', 'Government Hospital'), ('private', 'Private Hospital')], max_length=20, null=True)),
                ('address', models.TextField(null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('latitude', models.CharField(max_length=100, null=True)),
                ('longitude', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='HospitalModel',
        ),
        migrations.DeleteModel(
            name='PoliceStationModel',
        ),
    ]
