# Generated by Django 5.0.6 on 2024-06-28 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship', '0013_alter_mentor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
