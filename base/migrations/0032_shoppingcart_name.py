# Generated by Django 4.0.6 on 2022-08-28 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_shoppingcart_user_shoppingcart'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
