"""
This module provides a set of classes for building forms in Django
"""
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils import timezone

from core.constants import PRESENT_TYPES, TASK_TYPES
from hubble import models
from hubble.models import Assessment


class TimelineForm(forms.ModelForm):
    """
    Timeline form is used to create or update timeline objects,
    with additional validation and customization for the form fields.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["team"].empty_label = "Select a Team"
        self.fields["name"].validators.append(MinLengthValidator(3))

    def clean(self):
        """
        The function checks if a timeline with the given ID exists and
        returns an error message if it does not.
        """
        cleaned_data = super().clean()
        if self.data.get("id") and (
            not models.Timeline.objects.filter(id=self.data.get("id")).exists()
        ):
            self.add_error(None, "You are trying to duplicate invalid template")
        return cleaned_data

    def clean_is_active(self):
        """
        This function checks if a team already has an active template
        and raises a validation error if it does.
        """
        if self.cleaned_data.get("team", None) and (self.cleaned_data["is_active"]):
            query = models.Timeline.objects.filter(
                team=self.cleaned_data["team"], is_active=True
            ).values("id")
            if (len(query)) and (query[0]["id"] != (self.instance.id)):
                raise ValidationError(
                    "Team already has an active template.",
                    code="template_in_use",
                )

    class Meta:
        """
        Meta class for defining class behavior and properties.
        """

        model = models.Timeline
        fields = ("name", "team", "is_active")

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full block border border-primary-dark-30 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2",
                    "placeholder": "Timeline name...",
                }
            ),
            "team": forms.Select(
                attrs={
                    "class": "w-full block border border-primary-dark-30 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2 dropdown_select",
                    "placeholder": "Select Team...",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "checkbox_active cursor-pointer block border \
                        border-primary-dark-30 rounded-md w-4 mr-3 focus:outline-none \
                            focus:ring-transparent focus:ring-offset-0 h-9 p-2",
                }
            ),
        }


class TimelineTaskForm(forms.ModelForm):
    """
    Timeline task form is used to add and update the timeline task
    with the respective with the custom validations
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].validators.append(MinLengthValidator(3))

    @staticmethod
    def validate_days(value):
        """
        The function validates that a given value is greater than 0 and
        a multiple of 0.5, otherwise it raises a validation error.
        """
        if value <= 0:
            raise ValidationError(
                "Value must be greater than 0",
                code="value_cannot_be_zero",
            )
        if value % 0.5 != 0:
            raise ValidationError(
                "Value must be a multiple of 0.5",
                code="is_not_divisible_by_0.5",
            )

    days = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "w-full block border border-primary-dark-30 \
                    rounded-md focus:outline-none focus:ring-transparent \
                        focus:ring-offset-0 h-9 p-2",
                "placeholder": "No of days...",
            }
        ),
        validators=[validate_days],
    )
    present_type = forms.ChoiceField(
        error_messages={
            "invalid_choice": "Select a valid choice. "
            "That choice is not one of the available choices."
        },
        widget=forms.RadioSelect,
        choices=PRESENT_TYPES,
    )
    task_type = forms.ChoiceField(
        error_messages={
            "invalid_choice": "Select a valid choice. "
            "That choice is not one of the available choices."
        },
        widget=forms.RadioSelect,
        choices=TASK_TYPES,
    )

    class Meta:
        """
        Meta class for defining class behavior and properties.
        """

        model = models.TimelineTask
        fields = ("name", "days", "present_type", "task_type")

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full block border border-primary-dark-30 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2",
                    "placeholder": "Timeline name...",
                }
            ),
        }


class BatchForm(forms.ModelForm):
    """
    Batch form is used to create and update the batch data
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].validators.append(MinLengthValidator(3))

    class Meta:
        """
        Meta class for defining class behavior and properties.
        """

        model = models.Batch
        fields = ("name",)

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full block border border-primary-dark-30 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2",
                    "placeholder": "Batch Name...",
                }
            )
        }


class SubBatchForm(forms.ModelForm):
    """
    Sub batch form is used to create and update the sub batch with custom validations
    """

    primary_mentor_id = forms.ModelChoiceField(
        queryset=models.User.objects.filter(is_employed=True)
    )

    secondary_mentor_ids = forms.ModelMultipleChoiceField(
        queryset=models.User.objects.filter(is_employed=True),
        error_messages={
            "invalid_choice": "Select a valid choice. That choice is not one of the available choices."
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["team"].empty_label = "Select a Team"
        if self.data.get("team", None):
            self.fields["team"].widget.attrs["initialValue"] = self.data.get("team", None)

        self.fields["primary_mentor_id"].empty_label = "Select a Primary Mentor"
        if self.data.get("primary_mentor_id", None):
            self.fields["primary_mentor_id"].widget.attrs["initialValue"] = self.data.get(
                "primary_mentor_id", None
            )

        if self.data.get("secondary_mentor_ids", None):
            self.fields["secondary_mentor_ids"].widget.attrs["initialValue"] = self.data.get(
                "secondary_mentor_ids", None
            )

        self.fields["name"].validators.append(MinLengthValidator(3))
        self.fields["primary_mentor_id"].label = "Primary Mentor"
        self.fields["secondary_mentor_ids"].label = "Secondary Mentors"
        self.fields["secondary_mentor_ids"].widget.attrs["subtitle"] = "Secondary Mentors"

        if kwargs.get("instance"):
            instance = kwargs.get("instance")
            self.fields["team"].widget.attrs["initialValue"] = instance.team
            self.fields["primary_mentor_id"].widget.attrs[
                "initialValue"
            ] = instance.primary_mentor_id
            self.fields["secondary_mentor_ids"].widget.attrs[
                "initialValue"
            ] = instance.secondary_mentors.all().values_list("id", flat=True)

    def clean_timeline(self):
        """
        The function checks if a selected team's active timeline
        has any tasks and raises a validation error if it doesn't.
        """
        if not models.TimelineTask.objects.filter(timeline=self.cleaned_data["timeline"].id):
            raise ValidationError(
                "The Selected Team's Active Timeline doesn't have any tasks.",
                code="timeline_has_no_tasks",
            )
        return self.cleaned_data["timeline"]

    def clean_start_date(self):
        if (
            models.Holiday.objects.filter(date_of_holiday=self.cleaned_data["start_date"]).exists()
            or self.cleaned_data["start_date"].weekday() == 6
        ):
            raise ValidationError(
                "The Selected date falls on a holiday, please reconsider the start date",
                code="invalid_date",
            )
        return self.cleaned_data["start_date"]

    class Meta:
        """
        Meta class for defining class behavior and properties.
        """

        model = models.SubBatch
        fields = (
            "name",
            "team",
            "start_date",
            "timeline",
            "primary_mentor_id",
            "secondary_mentor_ids",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full block border border-primary-dark-30 mt-2.5 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2 bg-transparent w-250 ",
                    "placeholder": "Batch Name...",
                }
            ),
            "team": forms.Select(
                attrs={
                    "class": "w-full block border border-primary-dark-30 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2 dropdown_select bg-transparent w-250",
                    "placeholder": "Select Team...",
                }
            ),
            "start_date": forms.DateInput(
                attrs={
                    "class": "block border border-primary-dark-30 \
                        rounded-md mt-2.5 w-64 focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2 bg-transparent w-250 start_date_input",
                    "placeholder": "Start Date...",
                }
            ),
            "timeline": forms.TextInput(
                attrs={
                    "class": "w-full block border border-primary-dark-30 mt-2.5 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2 bg-transparent w-250 timeline-input",
                }
            ),
            "primary_mentor_id": forms.Select(
                attrs={
                    "class": "w-full block border border-primary-dark-30 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2 dropdown_select bg-transparent w-250",
                    "placeholder": "Primary Mentor...",
                }
            ),
            "secondary_mentor_ids": forms.SelectMultiple(
                attrs={
                    "class": "w-full block border border-primary-dark-30 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2 dropdown_select bg-transparent w-250",
                    "placeholder": "Secondary Mentors...",
                }
            ),
        }


class AddInternForm(forms.ModelForm):
    """
    Add intern for is used to add the trainee in the sub-batch
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["college"].validators.append(MinLengthValidator(3))
        self.fields["user_id"].empty_label = "Select a Trainee"

    def clean(self):
        """
        The function checks if a given sub_batch_id exists in the
        database and adds an error message if it does not.
        """
        cleaned_data = super().clean()
        if self.data.get("sub_batch_id") and not (
            models.SubBatch.objects.filter(id=self.data.get("sub_batch_id")).exists()
        ):
            self.add_error(
                None,
                "You are trying to add trainees to an invalid SubBatch",
            )
        return cleaned_data

    def clean_user_id(self):
        """
        The function checks if a user ID already exists in the InternDetail model and raises a
        validation error if it does.
        """
        if models.InternDetail.objects.filter(user=self.cleaned_data["user_id"]).exists():
            raise ValidationError(
                "Trainee already added in the another sub-batch",
                code="trainee_exists",
            )

    user_id = forms.ModelChoiceField(
        queryset=(
            models.User.objects.exclude(
                intern_details__isnull=False, intern_details__deleted_at__isnull=True
            ).filter(is_employed=False)
        ),
        label="User",
    )

    class Meta:
        """
        Meta class for defining class behavior and properties.
        """

        model = models.InternDetail
        fields = ("user_id", "college")

        widgets = {
            "college": forms.TextInput(
                attrs={
                    "class": "w-full block border border-primary-dark-30 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2",
                    "placeholder": "College name...",
                }
            ),
            "user_id": forms.Select(
                attrs={
                    "class": "w-full block border border-primary-dark-30 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2 dropdown_select bg-transparent w-250",
                    "placeholder": "Trainee...",
                }
            ),
        }


class SubBatchTimelineForm(forms.ModelForm):
    """
    Sub batch timeline form is used to create and update the sub-batch tasks
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].validators.append(MinLengthValidator(3))

    @staticmethod
    def validate_days(value):
        """
        The function validates that a given value is greater than 0 \
            and a multiple of 0.5, otherwise it
        raises a validation error.
        """
        if value <= 0:
            raise ValidationError(
                "Value must be greater than 0",
                code="value_cannot_be_zero",
            )
        if value % 0.5 != 0:
            raise ValidationError(
                "Value must be a multiple of 0.5",
                code="is_not_divisible_by_0.5",
            )

    def clean_order(self):
        """
        The function clean_order checks if the input order value is valid and returns it if it is.
        """
        valid_order_value = list(
            models.SubBatchTaskTimeline.objects.filter(
                start_date__gt=timezone.now(),
                sub_batch_id=self.data.get("sub_batch_id"),
            ).values_list("order", flat=True)
        ) or [0]
        if (valid_order_value[0] > self.cleaned_data["order"] > 0) or (
            self.cleaned_data["order"] > valid_order_value[-1] + 1
        ):
            raise ValidationError(
                (
                    f"The current order of the task is invalid. "
                    f"The valid input for order ranges form {valid_order_value[0]}-{valid_order_value[-1] + 1}."
                ),
                code="invalid_order",
            )
        if self.cleaned_data["order"] <= 0:
            raise ValidationError(
                "Order value must be greater than zero.",
                code="zero_order_error",
            )
        return self.cleaned_data["order"]

    days = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "w-full block border border-primary-dark-30 \
                    rounded-md focus:outline-none focus:ring-transparent \
                        focus:ring-offset-0 h-9 p-2",
                "placeholder": "Days...",
            }
        ),
        validators=[validate_days],
    )
    order = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "w-full block border border-primary-dark-30 \
                    rounded-md focus:outline-none focus:ring-transparent \
                        focus:ring-offset-0 h-9 p-2",
                "placeholder": "Order...",
                "required": False,
            }
        ),
    )
    present_type = forms.ChoiceField(
        error_messages={
            "invalid_choice": "Select a valid choice. "
            "That choice is not one of the available choices."
        },
        widget=forms.RadioSelect,
        choices=PRESENT_TYPES,
    )
    task_type = forms.ChoiceField(
        error_messages={
            "invalid_choice": "Select a valid choice. "
            "That choice is not one of the available choices."
        },
        widget=forms.RadioSelect,
        choices=TASK_TYPES,
    )

    class Meta:
        """
        Meta class for defining class behavior and properties.
        """

        model = models.SubBatchTaskTimeline
        fields = ("name", "days", "present_type", "task_type", "order")

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full block border border-primary-dark-30 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2",
                    "placeholder": "Task Name...",
                }
            ),
        }


class InternScoreForm(forms.ModelForm):
    """
    Intenr score form is used to add the assessment mark details for the particular trainee
    """

    def clean_score(self):
        """
        The function `clean_score` validates that the score is between 0 and 100 and raises a
        `ValidationError` if it is not.
        """
        if not 0 <= self.cleaned_data["score"] <= 100:
            raise ValidationError("Score must be between 0 to 100", code="invalid_score")
        return self.cleaned_data["score"]

    class Meta:
        """
        Meta class for defining class behavior and properties.
        """

        model = Assessment
        fields = ("score", "is_retry", "comment")

        widgets = {
            "score": forms.NumberInput(
                attrs={
                    "class": "w-full block border border-primary-dark-30 \
                        rounded-md focus:outline-none focus:ring-transparent \
                            focus:ring-offset-0 h-9 p-2",
                    "placeholder": "Enter score...",
                }
            ),
            "is_retry": forms.CheckboxInput(
                attrs={
                    "class": "checkbox_active cursor-pointer block border \
                        border-primary-dark-30 rounded-md w-4 mr-3 focus:outline-none \
                            focus:ring-transparent focus:ring-offset-0 h-9 p-2",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "w-full block border border-primary-dark-30 \
                        rounded-md mt-2.5 w-64 focus:outline-none \
                            focus:ring-transparent focus:ring-offset-0 h-20 p-2 ",
                    "placeholder": "Enter comment...",
                }
            ),
        }
