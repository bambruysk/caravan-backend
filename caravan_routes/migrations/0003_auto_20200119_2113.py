# Generated by Django 3.0.2 on 2020-01-19 18:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('caravan_routes', '0002_caravan'),
    ]

    operations = [
        migrations.AddField(
            model_name='caravan',
            name='last_connect_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='route',
            name='last_update',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='RouteCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.BigIntegerField()),
                ('routes', models.ManyToManyField(to='caravan_routes.Route')),
            ],
        ),
    ]
