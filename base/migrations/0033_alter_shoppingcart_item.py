# Generated by Django 4.0.6 on 2022-08-28 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0032_shoppingcart_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='item',
            field=models.ManyToManyField(null=True, to='base.shopitem'),
        ),
    ]
