# Generated by Django 5.0.6 on 2024-06-26 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_alter_quiz_chapter_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizquestion',
            name='solved_status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='quizquestionattemptint',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='quizquestionattemptmmcq',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='quizquestionattemptsmcq',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
