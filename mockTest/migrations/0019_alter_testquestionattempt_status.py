# Generated by Django 5.0.6 on 2024-06-17 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mockTest', '0018_alter_testquestionattempt_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testquestionattempt',
            name='status',
            field=models.CharField(choices=[('Unattempted', 'Unattempted'), ('Skipped', 'Skipped'), ('Attempted', 'Attempted')], max_length=64, null=True),
        ),
    ]
