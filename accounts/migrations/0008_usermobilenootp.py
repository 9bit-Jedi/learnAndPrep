# Generated by Django 5.0.6 on 2024-07-02 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_user_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMobileNoOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_identifier', models.TextField(blank=True, null=True)),
                ('mobile_no', models.CharField(max_length=128)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('otp_created_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
