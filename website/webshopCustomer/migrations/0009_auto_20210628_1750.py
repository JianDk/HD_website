# Generated by Django 3.1.3 on 2021-06-28 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshopCustomer', '0008_auto_20210628_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='orderCreationDateTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]