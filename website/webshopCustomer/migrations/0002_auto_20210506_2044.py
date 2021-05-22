# Generated by Django 3.1.3 on 2021-05-06 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshopCustomer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='delivery',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='newsletter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='pickup',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='session_id',
            field=models.CharField(default=True, max_length=100),
            preserve_default=False,
        ),
    ]