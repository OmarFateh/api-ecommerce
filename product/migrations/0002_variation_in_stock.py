# Generated by Django 2.2 on 2021-03-25 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
    ]