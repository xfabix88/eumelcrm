# Generated by Django 5.0.6 on 2024-07-05 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crmsystem', '0008_alter_position_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='invoice',
        ),
    ]
