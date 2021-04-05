# Generated by Django 3.1.3 on 2021-04-05 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('allergic_note', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=0, default=0.0, max_digits=9)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deliverable', models.BooleanField(default=True)),
                ('image_path', models.ImageField(upload_to='productImages')),
                ('meta_keywords', models.CharField(help_text='comma delimited keywords text for SEO', max_length=255)),
                ('meta_description', models.CharField(help_text='SEO description content', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(help_text='Unique text for url created from name', max_length=255, unique=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_bestseller', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'products',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('meta_keywords', models.CharField(help_text='Comma delimited words for SEO purpose', max_length=255, verbose_name='Meta keywords')),
                ('meta_description', models.CharField(help_text='Content for meta tag description', max_length=255, verbose_name='Meta description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('products', models.ManyToManyField(to='webshopCatalog.Product')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
                'ordering': ['-created_at'],
            },
        ),
    ]
