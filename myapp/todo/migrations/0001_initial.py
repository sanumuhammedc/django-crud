# Generated by Django 4.1.6 on 2023-05-23 06:00

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.CharField(blank=True, max_length=200, null=True)),
                ("title", models.CharField(blank=True, max_length=200, null=True)),
                ("complete", models.BooleanField(default=False)),
                ("created", models.DateTimeField(default="2023-05-23 06:00")),
                ("deadline", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
    ]