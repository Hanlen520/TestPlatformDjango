# Generated by Django 3.1.3 on 2021-07-20 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('automated_main', '0014_auto_20210719_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apitestcase',
            name='api_key_variable',
        ),
        migrations.RemoveField(
            model_name='apitestcase',
            name='api_value_variable',
        ),
        migrations.RemoveField(
            model_name='apitestcase',
            name='api_variable_results',
        ),
    ]