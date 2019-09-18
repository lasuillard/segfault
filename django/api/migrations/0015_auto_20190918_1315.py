# Generated by Django 2.2.5 on 2019-09-18 04:15

from django.db import migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20190918_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='is_selected',
        ),
        migrations.AddField(
            model_name='answer',
            name='date_selected',
            field=model_utils.fields.MonitorField(blank=True, default=None, editable=False, monitor='status', null=True, when={'SELECTED'}),
        ),
        migrations.AddField(
            model_name='answer',
            name='status',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='SUGGESTED', max_length=100, no_check_for_status=True),
        ),
    ]
