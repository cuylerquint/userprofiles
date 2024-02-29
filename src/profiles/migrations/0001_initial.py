# Generated by Django 5.0 on 2024-02-29 18:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("created_dttm", models.DateTimeField(auto_now_add=True)),
                ("updated_dttm", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("phone", models.CharField(max_length=100, null=True)),
                ("unique_id", models.UUIDField(unique=True)),
            ],
            options={
                "ordering": ["-created_dttm"],
            },
        ),
        migrations.CreateModel(
            name="UpdateEmailToken",
            fields=[
                (
                    "key",
                    models.CharField(
                        editable=False, max_length=6, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("email", models.CharField(max_length=256)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="update_email_token",
                        to="profiles.userprofile",
                    ),
                ),
            ],
            options={
                "verbose_name": "update-email-token",
                "verbose_name_plural": "update-email-token",
                "db_table": "update_email_token",
            },
        ),
        migrations.CreateModel(
            name="AuthToken",
            fields=[
                (
                    "key",
                    models.CharField(
                        editable=False,
                        max_length=256,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="auth_token",
                        to="profiles.userprofile",
                    ),
                ),
            ],
            options={
                "verbose_name": "active-auth-token",
                "verbose_name_plural": "active-auth-tokens",
                "db_table": "active_auth_token",
            },
        ),
    ]