# Generated by Django 4.0.6 on 2022-08-27 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_alter_shopitem_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopItemSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
    ]