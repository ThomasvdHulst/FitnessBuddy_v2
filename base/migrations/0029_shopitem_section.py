# Generated by Django 4.0.6 on 2022-08-27 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_shopitemsection'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopitem',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.shopitemsection'),
        ),
    ]
