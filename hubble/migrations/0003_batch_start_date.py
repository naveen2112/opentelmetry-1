# Generated by Django 4.1.7 on 2023-08-08 16:38

import datetime
from django.db import migrations, models


def add_start_date_to_existing_batch(apps, schema_editor):
    Batch = apps.get_model("hubble", "Batch")
    for batch in Batch.objects.all():
        oldest_start_date = batch.sub_batches.order_by("start_date").values_list("start_date", flat=True).first()
        if oldest_start_date:
            batch.start_date = oldest_start_date
            batch.save()

class Migration(migrations.Migration):

    dependencies = [
        ('hubble', '0002_alter_assessment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 8, 16, 38, 21, 651420)),
            preserve_default=False,
        ),
        migrations.RunPython(add_start_date_to_existing_batch),
    ]
