# Generated by Django 5.0.6 on 2024-07-06 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmsystem', '0009_remove_position_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='show_diagnose',
            field=models.BooleanField(blank=True, default='False'),
        ),
    ]
