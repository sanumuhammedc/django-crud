# Generated by Django 4.1.6 on 2023-05-24 04:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="deadline",
        ),
        migrations.AlterField(
            model_name="task",
            name="created",
            field=models.DateTimeField(default="2023-05-24 04:57"),
        ),
    ]