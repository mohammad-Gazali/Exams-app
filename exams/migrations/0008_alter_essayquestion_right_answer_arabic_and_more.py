# Generated by Django 4.1.7 on 2023-04-06 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exams", "0007_alter_choiceanswer_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="essayquestion",
            name="right_answer_arabic",
            field=models.TextField(verbose_name="right answer arabic"),
        ),
        migrations.AlterField(
            model_name="essayquestion",
            name="right_answer_english",
            field=models.TextField(verbose_name="right answer english"),
        ),
    ]
