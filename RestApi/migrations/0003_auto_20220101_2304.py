# Generated by Django 3.1.7 on 2022-01-01 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestApi', '0002_officialvacations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialvacations',
            name='date',
            field=models.DateField(),
        ),
    ]
