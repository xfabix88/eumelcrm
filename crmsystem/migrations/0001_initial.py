# Generated by Django 5.0.6 on 2024-07-05 09:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Claims',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(max_length=100)),
                ('customer_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, max_length=20)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('sex', models.CharField(blank=True, max_length=10)),
                ('birthday', models.CharField(blank=True, max_length=50)),
                ('mail', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('mobile', models.CharField(blank=True, max_length=50)),
                ('street', models.CharField(blank=True, max_length=100)),
                ('housenumber', models.CharField(blank=True, max_length=50)),
                ('plz', models.CharField(blank=True, max_length=15)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('country', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.CharField(blank=True, max_length=100)),
                ('note', models.TextField(blank=True, max_length=100)),
                ('customer', models.CharField(blank=True, max_length=100)),
                ('day', models.DateField(blank=True, default='2024-05-22')),
                ('time_begin', models.TimeField(blank=True, default='10:00')),
                ('time_end', models.TimeField(blank=True, default='11:00')),
                ('text', models.TextField(blank=True, max_length=10000)),
                ('googlecalendar', models.CharField(blank=True, max_length=1000)),
                ('invoice', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=100)),
                ('customer', models.CharField(blank=True, max_length=100)),
                ('date_begin', models.DateField(blank=True, default='2024-05-22')),
                ('date_end', models.DateField(blank=True, default='2024-05-22')),
                ('product', models.CharField(blank=True, max_length=100)),
                ('text', models.CharField(blank=True, max_length=100)),
                ('price', models.CharField(blank=True, max_length=100)),
                ('reci_title', models.CharField(blank=True, max_length=20)),
                ('reci_first_name', models.CharField(max_length=100)),
                ('reci_last_name', models.CharField(max_length=100)),
                ('reci_street', models.CharField(blank=True, max_length=100)),
                ('reci_housenumber', models.CharField(blank=True, max_length=50)),
                ('reci_plz', models.CharField(blank=True, max_length=15)),
                ('reci_city', models.CharField(blank=True, max_length=100)),
                ('reci_country', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Position3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=255)),
                ('price', models.IntegerField(max_length=255)),
                ('count', models.IntegerField(max_length=255)),
                ('endprice', models.CharField(max_length=255)),
                ('factor', models.IntegerField(blank=True)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crmsystem.date')),
            ],
        ),
    ]
