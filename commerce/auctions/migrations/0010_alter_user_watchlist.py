# Generated by Django 4.2.4 on 2023-08-22 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_user_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, default=None, to='auctions.listing'),
        ),
    ]