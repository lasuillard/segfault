# Generated by Django 2.2.5 on 2019-09-19 02:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0016_auto_20190918_1518'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChatRoom',
            new_name='Room',
        ),
    ]