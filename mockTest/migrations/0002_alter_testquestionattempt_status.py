# Generated by Django 5.0.6 on 2024-06-13 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mockTest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testquestionattempt',
            name='status',
            field=models.CharField(choices=[('Attempted', 'Attempted'), ('Skipped', 'Skipped'), ('Unattempted', 'Unattempted')], max_length=64, null=True),
        ),
    ]