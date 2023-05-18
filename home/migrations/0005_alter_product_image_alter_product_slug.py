# Generated by Django 4.2 on 2023-05-07 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='product/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=200),
        ),
    ]