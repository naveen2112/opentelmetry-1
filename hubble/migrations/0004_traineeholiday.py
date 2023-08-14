# Generated by Django 4.1.7 on 2023-08-08 17:55

import core.db
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from core.constants import BATCH_DURATION
from dateutil.relativedelta import relativedelta


def add_holidays_to_existing_batches(apps, schema_editor):
    Batch = apps.get_model("hubble", "Batch")
    TraineeHoliday = apps.get_model("hubble", "TraineeHoliday")
    Holiday = apps.get_model("hubble", "Holiday")
    for batch in Batch.objects.all():
        start_date = batch.start_date
        end_date = start_date + relativedelta(months=BATCH_DURATION)
        holidays = Holiday.objects.filter(
            date_of_holiday__range=(start_date, end_date)
        )
        trainee_holidays = [
            TraineeHoliday(
                batch_id = batch.id,
                date_of_holiday = holiday.date_of_holiday,
                month_year = holiday.month_year,
                updated_by = batch.created_by,
                reason = holiday.reason,
                national_holiday = holiday.national_holiday,
                allow_check_in = holiday.allow_check_in
            )
            for holiday in holidays
        ]
        TraineeHoliday.objects.bulk_create(trainee_holidays)

class Migration(migrations.Migration):

    dependencies = [
        ('hubble', '0003_batch_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='national_holiday',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='TraineeHoliday',
            fields=[
                ('created_at', core.db.DateTimeWithoutTZField(auto_now_add=True)),
                ('updated_at', core.db.DateTimeWithoutTZField(auto_now=True)),
                ('deleted_at', core.db.DateTimeWithoutTZField(null=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_of_holiday', models.DateField()),
                ('month_year', models.CharField(max_length=255)),
                ('reason', models.CharField(max_length=255)),
                ('national_holiday', models.BooleanField()),
                ('allow_check_in', models.BooleanField()),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holidays', to='hubble.batch')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'trainee_holidays',
                'managed': True,
            },
        ),
        migrations.RunPython(add_holidays_to_existing_batches),
    ]
