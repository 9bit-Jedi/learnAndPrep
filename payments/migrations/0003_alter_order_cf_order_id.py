# Generated by Django 5.0.6 on 2024-08-11 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_order_order_amount_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cf_order_id',
            field=models.CharField(max_length=255),
        ),
    ]
