# Generated by Django 2.2.5 on 2019-09-10 07:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_delete_producer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=30, validators=[django.core.validators.ProhibitNullCharactersValidator()]),
        ),
    ]
