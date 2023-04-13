# Generated by Django 4.1.7 on 2023-04-04 12:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0006_alter_essayquestion_question_arabic_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choiceanswer',
            options={'ordering': ['-created_at'], 'verbose_name': 'choice', 'verbose_name_plural': 'choices'},
        ),
        migrations.AlterModelOptions(
            name='essayquestion',
            options={'ordering': ['-created_at'], 'verbose_name': 'essay question', 'verbose_name_plural': 'essay questions'},
        ),
        migrations.AlterModelOptions(
            name='exam',
            options={'ordering': ['-created_at'], 'verbose_name': 'exam', 'verbose_name_plural': 'exams'},
        ),
        migrations.AlterModelOptions(
            name='multiplechoicequestion',
            options={'ordering': ['-created_at'], 'verbose_name': 'MCQ', 'verbose_name_plural': 'MCQs'},
        ),
        migrations.AlterModelOptions(
            name='truefalsequestion',
            options={'ordering': ['-created_at'], 'verbose_name': 'true-false question', 'verbose_name_plural': 'true-false questions'},
        ),
        migrations.AddField(
            model_name='choiceanswer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='choiceanswer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AddField(
            model_name='essayquestion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='essayquestion',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AddField(
            model_name='truefalsequestion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='truefalsequestion',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
    ]