# Generated by Django 5.1.4 on 2024-12-18 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='response',
            field=models.BooleanField(default=False),
        ),
    ]
