# Generated by Django 4.2.4 on 2023-08-13 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(default='Home', max_length=64),
            preserve_default=False,
        ),
    ]