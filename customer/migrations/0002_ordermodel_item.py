# Generated by Django 3.2.15 on 2022-09-28 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='item',
            field=models.ManyToManyField(blank=True, related_name='order', to='customer.MenuItem'),
        ),
    ]
