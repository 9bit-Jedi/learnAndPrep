# Generated by Django 5.0.6 on 2024-05-28 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='value',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='topic',
            name='value',
            field=models.CharField(max_length=128),
        ),
    ]
