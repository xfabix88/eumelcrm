# Generated by Django 5.0.6 on 2024-07-05 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmsystem', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.AlterField(
            model_name='date',
            name='product',
            field=models.CharField(blank=True, choices=[('B30', 'Bioresonanz 30 Minuten'), ('B60', 'Bioresonanz 60 Minuten'), ('B90', 'Bioresonanz 90 Minuten'), ('P60', 'Psychotherapie 60 Minuten'), ('P90', 'Psychotherapie 90 Minuten'), ('E01', 'Erstgespräch')], max_length=100),
        ),
        migrations.DeleteModel(
            name='Position3',
        ),
    ]
