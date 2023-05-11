from django.db import models
from hubble.models import User
from .project import Project
from . import ProjectResourcePosition


class ProjectResource(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, models.CASCADE, blank=True, null=True, related_name="project_resource"
    )
    project = models.ForeignKey(
        Project, models.CASCADE, blank=True, null=True, related_name="project"
    )
    reporting_person = models.ForeignKey(
        User, models.CASCADE, blank=True, null=True, related_name="reporting_person"
    )
    resource_type = models.CharField(max_length=255, blank=True, null=True)
    utilisation = models.IntegerField(blank=True, null=True)
    charge_by_hour = models.FloatField(blank=True, null=True)
    primary_project = models.BooleanField(blank=True, null=True)
    allotted_from = models.DateField(blank=True, null=True)
    removed_on = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    position = models.ForeignKey(
        ProjectResourcePosition,
        models.DO_NOTHING,
        db_column="position",
        blank=True,
        null=True,
        related_name="position",
    )

    class Meta:
        managed = False
        db_table = "project_resources"
