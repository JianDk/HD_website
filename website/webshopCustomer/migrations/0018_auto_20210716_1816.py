# Generated by Django 3.1.3 on 2021-07-16 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshopCustomer', '0017_auto_20210628_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='latitude',
            field=models.CharField(default=100000, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='longitude',
            field=models.CharField(default=10000, max_length=50),
            preserve_default=False,
        ),
    ]
