# Generated by Django 4.0.6 on 2022-07-20 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_exercise'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exercise',
            options={'ordering': ['name']},
        ),
    ]