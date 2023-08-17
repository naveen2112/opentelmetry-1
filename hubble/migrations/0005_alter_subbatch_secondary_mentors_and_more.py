# Generated by Django 4.1.7 on 2023-08-17 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("hubble", "0004_remove_subbatch_secondary_mentor_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subbatch",
            name="secondary_mentors",
            field=models.ManyToManyField(
                related_name="secondary_sub_batches", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="subbatch",
            name="timeline",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sub_batches",
                to="hubble.timeline",
            ),
        ),
        migrations.AlterField(
            model_name="timelinetask",
            name="present_type",
            field=models.CharField(
                choices=[("Remote", "Remote"), ("In-Person", "In-Person")],
                default="Remote",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="timelinetask",
            name="task_type",
            field=models.CharField(
                choices=[
                    ("Task", "Task"),
                    ("Assessment", "Assessment"),
                    ("Cultural Meet", "Cultural Meet"),
                ],
                default="Task",
                max_length=255,
            ),
        ),
    ]
