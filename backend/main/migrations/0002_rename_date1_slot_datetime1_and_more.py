# Generated by Django 4.2.9 on 2024-09-01 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='slot',
            old_name='date1',
            new_name='datetime1',
        ),
        migrations.RenameField(
            model_name='slot',
            old_name='date2',
            new_name='datetime2',
        ),
        migrations.RenameField(
            model_name='slot',
            old_name='Specialist',
            new_name='specialist',
        ),
    ]
