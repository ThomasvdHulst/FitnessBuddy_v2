# Generated by Django 4.0.6 on 2022-07-24 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_statement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='completed',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
