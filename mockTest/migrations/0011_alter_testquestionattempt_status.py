# Generated by Django 5.0.6 on 2024-06-17 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mockTest', '0010_alter_testquestionattempt_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testquestionattempt',
            name='status',
            field=models.CharField(choices=[('Skipped', 'Skipped'), ('Unattempted', 'Unattempted'), ('Attempted', 'Attempted')], max_length=64, null=True),
        ),
    ]
