# Generated by Django 2.2.3 on 2019-08-13 03:30

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_avatar_user_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='user_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]