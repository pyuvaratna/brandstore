# Generated by Django 3.0.3 on 2020-03-03 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
