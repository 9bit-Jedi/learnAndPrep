# Generated by Django 5.0.6 on 2024-06-29 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mockTest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testquestionattempt',
            name='status',
            field=models.CharField(choices=[('Unattempted', 'Unattempted'), ('Skipped', 'not visited'), ('Attempted', 'Attempted')], max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='testquestionattempt',
            name='test_attempt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_attempts', to='mockTest.testattempt'),
        ),
        migrations.AlterField(
            model_name='testquestionattempt',
            name='test_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mockTest.testquestion'),
        ),
    ]
