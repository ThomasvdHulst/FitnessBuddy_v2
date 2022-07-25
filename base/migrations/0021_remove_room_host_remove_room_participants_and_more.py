# Generated by Django 4.0.6 on 2022-07-25 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_user_is_email_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='host',
        ),
        migrations.RemoveField(
            model_name='room',
            name='participants',
        ),
        migrations.RemoveField(
            model_name='room',
            name='topic',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]