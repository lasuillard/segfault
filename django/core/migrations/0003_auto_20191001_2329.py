# Generated by Django 2.2.5 on 2019-10-01 14:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20191001_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]