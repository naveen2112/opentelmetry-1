# Generated by Django 4.1.7 on 2023-06-15 09:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import core.db


class Migration(migrations.Migration):
    initial = True

    is_test_case = settings.IS_TEST_CASE

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                (
                    "employee_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "email",
                    models.CharField(max_length=255, unique=True),
                ),
                (
                    "email_verified_at",
                    core.db.DateTimeWithoutTZField(blank=True, null=True),
                ),
                (
                    "password",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "username",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "is_employed",
                    models.BooleanField(blank=True, null=True),
                ),
                (
                    "remember_token",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("status", models.CharField(max_length=255)),
                (
                    "branch_id",
                    models.BigIntegerField(blank=True, null=True),
                ),
                (
                    "team_owner",
                    models.BooleanField(blank=True, null=True),
                ),
                (
                    "first_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "last_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("is_saturday_working", models.BooleanField()),
            ],
            options={
                "db_table": "users",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "state",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "country",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "zip",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "street",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "city",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "db_table": "clients",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                ("symbol", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "currencies",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="Designation",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "db_table": "designations",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="ExpectedUserEfficiency",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("expected_efficiency", models.FloatField()),
                ("effective_from", models.DateField()),
                (
                    "effective_to",
                    models.DateField(blank=True, null=True),
                ),
            ],
            options={
                "db_table": "expected_user_efficiencies",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="Holiday",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("date_of_holiday", models.DateField()),
                ("month_year", models.CharField(max_length=255)),
                (
                    "reason",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("allow_check_in", models.BooleanField()),
            ],
            options={
                "db_table": "holidays",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="Module",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "modules",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("project_id", models.FloatField()),
                ("name", models.CharField(max_length=255)),
                (
                    "icon_path",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "icon_updated_at",
                    core.db.DateTimeWithoutTZField(blank=True, null=True),
                ),
                ("status", models.CharField(max_length=255)),
                (
                    "version",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "billing_frequency",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "db_table": "projects",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="ProjectResource",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                (
                    "resource_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "utilisation",
                    models.IntegerField(blank=True, null=True),
                ),
                (
                    "charge_by_hour",
                    models.FloatField(blank=True, null=True),
                ),
                (
                    "primary_project",
                    models.BooleanField(blank=True, null=True),
                ),
                (
                    "allotted_from",
                    models.DateField(blank=True, null=True),
                ),
                ("removed_on", models.DateField(blank=True, null=True)),
            ],
            options={
                "db_table": "project_resources",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="ProjectResourcePosition",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "required_reporting_person",
                    models.BooleanField(blank=True, null=True),
                ),
                (
                    "type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "db_table": "project_resource_positions",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "description",
                    models.TextField(blank=True, null=True),
                ),
            ],
            options={
                "db_table": "tasks",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("started_at", models.DateField(blank=True, null=True)),
            ],
            options={
                "db_table": "teams",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="TimesheetEntry",
            fields=[
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("description", models.TextField()),
                ("entry_date", models.DateField()),
                ("working_hours", models.FloatField()),
                ("approved_hours", models.FloatField()),
                ("authorized_hours", models.FloatField()),
                ("billed_hours", models.FloatField()),
                (
                    "admin_comments",
                    models.TextField(blank=True, null=True),
                ),
            ],
            options={
                "db_table": "timesheet_entries",
                "managed": is_test_case,
            },
        ),
        migrations.CreateModel(
            name="Batch",
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
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                ("name", models.CharField(max_length=250)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "batches",
            },
        ),
        migrations.CreateModel(
            name="SubBatch",
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
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                ("name", models.CharField(max_length=250)),
                ("start_date", models.DateField()),
                (
                    "batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sub_batches",
                        to="hubble.batch",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "primary_mentor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="primary_sub_batches",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "secondary_mentor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="secondary_sub_batches",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hubble.team",
                    ),
                ),
            ],
            options={
                "db_table": "sub_batches",
            },
        ),
        migrations.CreateModel(
            name="Timeline",
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
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "is_active",
                    models.BooleanField(
                        blank=True,
                        default=False,
                        verbose_name="is_active",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hubble.team",
                    ),
                ),
            ],
            options={
                "db_table": "timelines",
            },
        ),
        migrations.CreateModel(
            name="TimelineTask",
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
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                ("name", models.CharField(max_length=250)),
                ("days", models.FloatField()),
                (
                    "present_type",
                    models.CharField(
                        choices=[
                            ("Remote", "Remote"),
                            ("In-Person", "In-Person"),
                        ],
                        default="Remote",
                        max_length=250,
                    ),
                ),
                (
                    "task_type",
                    models.CharField(
                        choices=[
                            ("Task", "Task"),
                            ("Assessment", "Assessment"),
                            ("Cultural Meet", "Cultural Meet"),
                        ],
                        default="Task",
                        max_length=250,
                    ),
                ),
                ("order", models.IntegerField(blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "timeline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_timeline",
                        to="hubble.timeline",
                    ),
                ),
            ],
            options={
                "db_table": "timeline_tasks",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="SubBatchTaskTimeline",
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
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                ("name", models.CharField(max_length=255)),
                ("days", models.FloatField()),
                (
                    "present_type",
                    models.CharField(
                        choices=[
                            ("Remote", "Remote"),
                            ("In-Person", "In-Person"),
                        ],
                        default="Remote",
                        max_length=255,
                    ),
                ),
                (
                    "task_type",
                    models.CharField(
                        choices=[
                            ("Task", "Task"),
                            ("Assessment", "Assessment"),
                            ("Cultural Meet", "Cultural Meet"),
                        ],
                        default="Task",
                        max_length=255,
                    ),
                ),
                (
                    "start_date",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                ("end_date", core.db.DateTimeWithoutTZField(null=True)),
                ("order", models.IntegerField(blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sub_batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_timelines",
                        to="hubble.subbatch",
                    ),
                ),
            ],
            options={
                "db_table": "sub_batch_timeline_tasks",
                "ordering": ["order"],
            },
        ),
        migrations.AddField(
            model_name="subbatch",
            name="timeline",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="hubble.timeline",
            ),
        ),
        migrations.CreateModel(
            name="InternDetail",
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
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                ("college", models.CharField(max_length=250)),
                ("expected_completion", models.DateField(null=True)),
                ("actual_completion", models.DateField(null=True)),
                ("comment", models.TextField(null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_intern_details",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sub_batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="intern_details",
                        to="hubble.subbatch",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="intern_details",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "intern_details",
            },
        ),
        migrations.CreateModel(
            name="Extension",
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
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_extensions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sub_batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="extensions",
                        to="hubble.subbatch",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="extensions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "extensions",
            },
        ),
        migrations.CreateModel(
            name="Assessment",
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
                (
                    "created_at",
                    core.db.DateTimeWithoutTZField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    core.db.DateTimeWithoutTZField(auto_now=True),
                ),
                (
                    "deleted_at",
                    core.db.DateTimeWithoutTZField(null=True),
                ),
                ("score", models.IntegerField()),
                ("is_retry", models.BooleanField(default=False)),
                ("comment", models.TextField()),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_assessments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "extension",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assessments",
                        to="hubble.extension",
                    ),
                ),
                (
                    "sub_batch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hubble.subbatch",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assessments",
                        to="hubble.subbatchtasktimeline",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assessments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "assessments",
            },
        ),
    ]
