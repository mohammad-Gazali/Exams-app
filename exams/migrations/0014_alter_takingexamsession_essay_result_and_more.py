# Generated by Django 4.1.7 on 2023-04-12 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0013_alter_takingexamsession_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='takingexamsession',
            name='essay_result',
            field=models.IntegerField(verbose_name='essay_result'),
        ),
        migrations.AlterField(
            model_name='takingexamsession',
            name='final_result',
            field=models.IntegerField(verbose_name='final_result'),
        ),
        migrations.AlterField(
            model_name='takingexamsession',
            name='mcq_result',
            field=models.IntegerField(verbose_name='mcq_result'),
        ),
        migrations.AlterField(
            model_name='takingexamsession',
            name='true_false_result',
            field=models.IntegerField(verbose_name='true_false_result'),
        ),
    ]