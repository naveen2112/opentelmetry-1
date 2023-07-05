# Generated by Django 4.1.7 on 2023-06-16 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("hubble", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assessment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assessments",
                to=settings.AUTH_USER_MODEL,
            ),
        )
    ]

    if settings.TESTING:
        operations.append(
            migrations.AddField(
                model_name="user",
                name="designation",
                field=models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    to="hubble.designation",
                ),
            )
        )
        operations.append(
            migrations.AddField(
                model_name="user",
                name="team",
                field=models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    to="hubble.team",
                ),
            )
        )
