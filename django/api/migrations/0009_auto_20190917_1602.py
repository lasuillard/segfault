# Generated by Django 2.2.5 on 2019-09-17 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20190917_1320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='avatar',
            old_name='user_data',
            new_name='extra_data',
        ),
    ]
