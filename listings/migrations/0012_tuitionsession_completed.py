# Generated by Django 3.1.6 on 2021-03-13 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0011_remove_tuitionsession_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuitionsession',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
