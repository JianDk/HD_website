# Generated by Django 3.1.3 on 2021-07-05 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshopRestaurant', '0010_auto_20210510_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='cvr',
            field=models.CharField(default=38908901, max_length=20),
            preserve_default=False,
        ),
    ]