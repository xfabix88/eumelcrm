# Generated by Django 5.0.6 on 2024-07-05 20:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmsystem', '0006_alter_position_factor'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='invoice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='crmsystem.invoice'),
            preserve_default=False,
        ),
    ]
