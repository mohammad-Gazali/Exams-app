# Generated by Django 4.1.7 on 2023-03-27 20:02

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='description_arabic',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='description arabic'),
        ),
        migrations.AddField(
            model_name='exam',
            name='description_english',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='description english'),
        ),
    ]
