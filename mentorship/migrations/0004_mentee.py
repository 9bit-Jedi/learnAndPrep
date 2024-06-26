# Generated by Django 5.0.6 on 2024-06-26 00:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship', '0003_alter_mentor_id_alter_mentor_medium'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=12)),
                ('state', models.CharField(max_length=48)),
                ('dropper_status', models.CharField(choices=[('Dropper', 'Dropper'), ('Non-dropper', 'Non-dropper')], max_length=28)),
                ('medium', models.CharField(choices=[('English', 'English'), ('Hindi', 'Hindi')], max_length=28)),
                ('did_you_change', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=28)),
                ('physics_rank', models.IntegerField()),
                ('chemistry_rank', models.IntegerField()),
                ('maths_rank', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
