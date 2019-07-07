# Generated by Django 2.2.3 on 2019-07-07 03:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='profile_image',
            field=models.FileField(upload_to='', validators=[django.core.validators.validate_image_file_extension]),
        ),
    ]
