# Generated by Django 4.2.15 on 2024-10-08 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_slotaction_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='is_deleted',
            field=models.BooleanField(default=False, help_text='Slot is deleted'),
        ),
    ]
