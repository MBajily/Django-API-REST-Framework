# Generated by Django 4.0.5 on 2022-06-07 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='date',
        ),
    ]
