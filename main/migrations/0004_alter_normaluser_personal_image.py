# Generated by Django 4.1.7 on 2023-03-27 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_remove_teacher_birthdate_remove_teacher_gender_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="normaluser",
            name="personal_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="personal_images",
                verbose_name="personal image",
            ),
        ),
    ]
