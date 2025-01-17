# Generated by Django 4.2.13 on 2024-07-04 05:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("code_submission", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CodeSubmission",
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
                ("code", models.TextField(verbose_name="提交的代码")),
                ("test_code", models.TextField(verbose_name="测试代码")),
                ("output", models.TextField(verbose_name="输出")),
                (
                    "submission_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="提交时间"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户",
                    ),
                ),
            ],
        ),
    ]
