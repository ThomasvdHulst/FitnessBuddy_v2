# Generated by Django 4.0.6 on 2022-07-24 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_statement_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='statements_list',
            field=models.ManyToManyField(to='base.statement'),
        ),
    ]
