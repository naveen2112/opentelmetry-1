import io

import pandas as pd
from django.conf import settings
from django.db.models import Count, Q
from django.forms.models import model_to_dict
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from model_bakery import baker
from model_bakery.recipe import seq

from core.base_test import BaseTestCase
from hubble.models import Batch, SubBatch, User
from training.forms import SubBatchForm


class SubBatchCreateTest(BaseTestCase):
    """
    This class is responsible for testing the CREATE feature in sub_batch module
    """

    create_route_name = "sub-batch.create"
    route_name = "batch.detail"

    def setUp(self):
        """
        This function will run before every test and makes sure required data are ready
        """
        super().setUp()
        self.authenticate()
        self.update_valid_input()

    def update_valid_input(self):
        """
        This function is responsible for updating the valid inputs and creating data in databases as reqiured
        """
        self.batch_id = baker.make("hubble.Batch").id
        baker.make(
            "hubble.User",
            is_employed=True,
            _fill_optional=["email"],
            employee_id=seq(0),
            _quantity=5,
        )
        baker.make(
            "hubble.User",
            is_employed=False,
            _fill_optional=["email"],
            employee_id=seq(5),
            _quantity=5,
        )
        primary_mentor_id = User.objects.get(employee_id=1).id
        secondary_mentor_id = User.objects.get(employee_id=2).id
        team_id = self.create_team().id
        timeline = baker.make("hubble.Timeline", team_id=team_id)
        baker.make(
            "hubble.TimelineTask",
            timeline_id=timeline.id,
            _fill_optional=["order"],
            _quantity=5,
            days=2,
        )
        baker.make(
            "hubble.Holiday",
            date_of_holiday=timezone.now().date() + timezone.timedelta(days=1),
        )
        self.persisted_valid_inputs = {
            "name": self.faker.name(),
            "team": team_id,
            "start_date": timezone.now().date(),
            "timeline": timeline.id,
            "primary_mentor_id": primary_mentor_id,
            "secondary_mentor_id": secondary_mentor_id,
        }

    def create_valid_file_input(self):
        """
        This function is responsible for creating valid file input
        """
        memory_file = io.BytesIO()

        df = pd.DataFrame(
            {
                "employee_id": [2, 3],
                "college": ["college1", "college2"],
            }
        )
        df.to_excel(memory_file, index=False)
        memory_file.seek(0)
        return memory_file
    
    def create_invalid_file_input1(self):
        """
        This function is responsible for creating invalid file input with invalid employee id
        """
        memory_file = io.BytesIO()

        df = pd.DataFrame(
            {
                "employee_id": [15, 16],
                "college": ["college1", "college2"],
            }
        )
        df.to_excel(memory_file, index=False)
        memory_file.seek(0)
        return memory_file
    
    def create_invalid_file_input2(self):
        """
        This function is responsible for creating invalid file input with invalid column name
        """
        memory_file = io.BytesIO()

        df = pd.DataFrame(
            {
                "employee_ids": [2, 3],
                "colleges": ["college1", "college2"],
            }
        )
        df.to_excel(memory_file, index=False)
        memory_file.seek(0)
        return memory_file

    def test_success(self):
        """
        Check what happens when valid data is given as input
        """
        data = self.get_valid_inputs({"users_list_file": self.create_valid_file_input()})
        response = self.make_post_request(
            reverse(self.create_route_name, args=[self.batch_id]),
            data=data,
        )
        self.assertRedirects(
            response, reverse(self.route_name, args=[self.batch_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertDatabaseHas(
            "SubBatch",
            {
                "name": data["name"],
                "team_id": data["team"],
                "timeline_id": data["timeline"],
                "start_date": data["start_date"],
            },
        )

    def test_required_validation(self):
        """
        This function checks the required validation for the team and name fields
        """
        data = {"users_list_file": self.create_valid_file_input()}
        self.make_post_request(
            reverse(self.create_route_name, args=[self.batch_id]),
            data=data,
        )
        field_errors = {
            "name": {"required"},
            "team": {"required"},
            "timeline": {"required"},
            "primary_mentor_id": {"required"},
            "secondary_mentor_id": {"required"},
        }
        self.validate_form_errors(
            field_errors=field_errors, form=SubBatchForm(data=data)
        )

    def test_invalid_choice_validation(self):
        """
        Check what happens when invalid data for team field is given as input
        """
        data = self.get_valid_inputs(
            {
                "users_list_file": self.create_valid_file_input(),
                "team": self.faker.name(),
                "timeline": self.faker.name(),
                "primary_mentor_id": self.faker.name(),
                "secondary_mentor_id": self.faker.name(),
            }
        )
        self.make_post_request(
            reverse(self.create_route_name, args=[self.batch_id]),
            data=data,
        )
        field_errors = {
            "team": {"invalid_choice"},
            "timeline": {"invalid_choice"},
            "primary_mentor_id": {"invalid_choice"},
            "secondary_mentor_id": {"invalid_choice"},
        }
        self.validate_form_errors(
            field_errors=field_errors, form=SubBatchForm(data=data)
        )

    def test_minimum_length_validation(self):
        """
        To check what happens when name field fails MinlengthValidation
        """
        data = self.get_valid_inputs(
            {
                "users_list_file": self.create_valid_file_input(),
                "name": self.faker.pystr(max_chars=2),
            }
        )
        self.make_post_request(
            reverse(self.create_route_name, args=[self.batch_id]),
            data=data,
        )
        field_errors = {"name": {"min_length"}}
        self.validate_form_errors(
            field_errors=field_errors,
            current_value=data,
            validation_parameter={"name": 3},
            form=SubBatchForm(data=data),
        )

    def test_invalid_start_date(self):
        """
        To check what happens when start_date is invalid
        """
        data = self.get_valid_inputs(
            {
                "users_list_file": self.create_valid_file_input(),
                "start_date": timezone.now().date() + timezone.timedelta(days=1),
            }
        )
        self.assertFormError(
            SubBatchForm(data=data),
            "start_date",
            "The Selected date falls on a holiday, please reconsider the start date",
        )

    def test_validate_no_timeline_task(self):
        """
        Check what happpens when a timeline with no task is selected
        """
        team_id = self.create_team().id
        timeline = baker.make("hubble.Timeline", team_id=team_id)
        data = self.get_valid_inputs(
            {
                "users_list_file": self.create_valid_file_input(),
                "team": team_id,
                "timeline": timeline.id,
            }
        )
        self.make_post_request(
            reverse(self.create_route_name, args=[self.batch_id]),
            data=data,
        )
        field_errors = {
            "timeline": {"timeline_has_no_tasks"},
        }
        self.validate_form_errors(
            field_errors=field_errors, form=SubBatchForm(data=data)
        )



    def test_file_validation(self):
        """
        To check what happens when file input isn't valid
        """
        # When file is not uploaded
        data = self.get_valid_inputs()
        response = self.make_post_request(
            reverse(self.create_route_name, args=[self.batch_id]),
            data=data,
        )
        self.assertEqual(
            strip_tags(response.context["errors"]),
            "Please upload a file",
        )

        # Invalid data in file interns belong to another sub-batch
        data = self.get_valid_inputs({"users_list_file": self.create_valid_file_input()})
        self.make_post_request(
            reverse(self.create_route_name, args=[self.batch_id]),
            data=data,
        )
        data = self.get_valid_inputs({"users_list_file": self.create_valid_file_input()})
        response = self.make_post_request(
            reverse(self.create_route_name, args=[self.batch_id]),
            data=data,
        )
        self.assertEqual(
            strip_tags(response.context["errors"]),
            "Some of the Users are already added in another sub-batch",
        )

        # Invalid data in file, employee_id doesn't match with any employee_id in db
        data = self.get_valid_inputs({"users_list_file": self.create_invalid_file_input1()})
        response = self.make_post_request(
            reverse(self.create_route_name, args=[self.batch_id]),
            data=data,
        )
        self.assertEqual(
            strip_tags(response.context["errors"]),
            "Some of the employee ids are not present in the database, please check again",
        )

        # Invalid column names are present
        data = self.get_valid_inputs({"users_list_file": self.create_invalid_file_input2()})
        response = self.make_post_request(
            reverse(self.create_route_name, args=[self.batch_id]),
            data=data,
        )
        self.assertEqual(
            strip_tags(response.context["errors"]),
            "Invalid keys are present in the file, please check the sample file",
        )


class SubBatchUpdateTest(BaseTestCase):
    """
    This class is responsible for testing the Edit feature in sub_batch module
    """

    update_route_name = "sub-batch.edit"
    route_name = "batch.detail"

    def setUp(self):
        """
        This function will run before every test and makes sure required data are ready
        """
        super().setUp()
        self.authenticate()
        self.update_valid_input()

    def update_valid_input(self):
        """
        This function is responsible for updating the valid inputs and creating data in databases as reqiured
        """
        self.batch_id = baker.make("hubble.Batch").id
        self.sub_batch_id = baker.make("hubble.SubBatch", batch_id=self.batch_id).id
        baker.make(
            "hubble.User",
            is_employed=True,
            _fill_optional=["email"],
            employee_id=seq(0),
            _quantity=5,
        )
        baker.make(
            "hubble.User",
            is_employed=False,
            _fill_optional=["email"],
            employee_id=seq(5),
            _quantity=5,
        )
        primary_mentor_id = User.objects.get(employee_id=1).id
        secondary_mentor_id = User.objects.get(employee_id=2).id
        team_id = self.create_team().id
        timeline = baker.make("hubble.Timeline", team_id=team_id)
        baker.make(
            "hubble.TimelineTask",
            timeline_id=timeline.id,
            _fill_optional=["order"],
            _quantity=5,
            days=2,
        )
        baker.make(
            "hubble.SubBatchTaskTimeline",
            days=2,
            order=1,
            sub_batch_id=self.sub_batch_id,
        )
        baker.make(
            "hubble.Holiday",
            date_of_holiday=timezone.now().date() + timezone.timedelta(days=1),
        )
        self.persisted_valid_inputs = {
            "name": self.faker.name(),
            "team": team_id,
            "start_date": timezone.now().date(),
            "timeline": timeline.id,
            "primary_mentor_id": primary_mentor_id,
            "secondary_mentor_id": secondary_mentor_id,
        }

    def test_success(self):
        """
        Check what happens when valid data is given as input
        """
        data = self.get_valid_inputs()
        response = self.make_post_request(
            reverse(self.update_route_name, args=[self.sub_batch_id]),
            data=data,
        )
        self.assertRedirects(response, reverse(self.route_name, args=[self.batch_id]))
        self.assertEqual(response.status_code, 302)
        self.assertDatabaseHas(
            "SubBatch",
            {
                "name": data["name"],
                "team_id": data["team"],
                "timeline_id": data["timeline"],
                "start_date": data["start_date"],
            },
        )

    def test_required_validation(self):
        """
        This function checks the required validation for the team and name fields
        """
        data = {}
        self.make_post_request(
            reverse(self.update_route_name, args=[self.sub_batch_id]),
            data=data,
        )
        field_errors = {
            "name": {"required"},
            "team": {"required"},
            "timeline": {"required"},
            "primary_mentor_id": {"required"},
            "secondary_mentor_id": {"required"},
        }
        self.validate_form_errors(
            field_errors=field_errors, form=SubBatchForm(data=data)
        )

    def test_invalid_choice_validation(self):
        """
        Check what happens when invalid data for team field is given as input
        """
        data = self.get_valid_inputs(
            {
                "team": self.faker.name(),
                "timeline": self.faker.name(),
                "primary_mentor_id": self.faker.name(),
                "secondary_mentor_id": self.faker.name(),
            }
        )
        self.make_post_request(
            reverse(self.update_route_name, args=[self.sub_batch_id]),
            data=data,
        )
        field_errors = {
            "team": {"invalid_choice"},
            "timeline": {"invalid_choice"},
            "primary_mentor_id": {"invalid_choice"},
            "secondary_mentor_id": {"invalid_choice"},
        }
        self.validate_form_errors(
            field_errors=field_errors, form=SubBatchForm(data=data)
        )

    def test_minimum_length_validation(self):
        """
        To check what happens when name field fails MinlengthValidation
        """
        data = self.get_valid_inputs({"name": self.faker.pystr(max_chars=2)})
        self.make_post_request(
            reverse(self.update_route_name, args=[self.sub_batch_id]),
            data=data,
        )
        field_errors = {"name": {"min_length"}}
        self.validate_form_errors(
            field_errors=field_errors,
            current_value=data,
            validation_parameter={"name": 3},
            form=SubBatchForm(data=data),
        )

    def test_invalid_start_date(self):
        """
        To check what happens when start_date is invalid
        """
        data = self.get_valid_inputs(
            {"start_date": timezone.now().date() + timezone.timedelta(days=1)}
        )
        self.assertFormError(
            SubBatchForm(data=data),
            "start_date",
            "The Selected date falls on a holiday, please reconsider the start date",
        )

    def test_timeline_has_no_tasks(self):
        """
        Check what happpens when a timeline with no task is selected
        """
        team_id = self.create_team().id
        timeline = baker.make("hubble.Timeline", team_id=team_id)
        data = self.get_valid_inputs({"team": team_id, "timeline": timeline.id})
        self.make_post_request(
            reverse(self.update_route_name, args=[self.sub_batch_id]),
            data=data,
        )
        field_errors = {
            "timeline": {"timeline_has_no_tasks"},
        }
        self.validate_form_errors(
            field_errors=field_errors, form=SubBatchForm(data=data)
        )


class SubBatchShowTest(BaseTestCase):
    """
    This class is responsible for testing the Show feature in sub_batch module
    """

    update_route_name = "sub-batch.edit"
    route_name = "batch.detail"

    def setUp(self):
        """
        This function will run before every test and makes sure required data are ready
        """
        super().setUp()
        self.authenticate()

    def test_success(self):
        """
        Check what happens when valid data is given as input
        """
        sub_batch = baker.make("hubble.SubBatch")
        response = self.make_get_request(
            reverse(self.update_route_name, args=[sub_batch.id])
        )
        self.assertIsInstance(response.context.get("form"), SubBatchForm)
        self.assertEqual(response.context.get("form").instance, sub_batch)

    def test_failure(self):
        """
        Check what happens when invalid data is given as input
        """
        response = self.make_get_request(reverse(self.update_route_name, args=[0]))
        self.assertEqual(
            self.bytes_cleaner(response.content),
            '{"message": "Invalid SubBatch id", "status": "error"}',
        )


class GetTimelineTest(BaseTestCase):
    """
    This class is responsible for testing whether correct timeline is fetched or not
    """

    get_timeline_route_name = "sub-batch.get_timeline"

    def setUp(self):
        """
        This function will run before every test and makes sure required data are ready
        """
        super().setUp()
        self.authenticate()

    def test_success(self):
        """
        Check what happens when valid data is given as input
        """
        team_id = baker.make("hubble.Team").id
        timeline = baker.make("hubble.Timeline", team_id=team_id, is_active=True)
        response = self.make_post_request(
            reverse(self.get_timeline_route_name),
            data={"team_id": team_id},
        )
        self.assertJSONEqual((response.content), {"timeline": model_to_dict(timeline)})
        self.assertEqual(response.status_code, 200)

    def test_failure(self):
        """
        Check what happens when invalid data is given as input
        """
        response = self.make_post_request(
            reverse(self.get_timeline_route_name), data={"team_id": 0}
        )
        self.assertJSONEqual(
            self.decoded_json(response),
            {
                "message": "No active timeline template found",
            },
        )
        self.assertEqual(response.status_code, 404)


class SubBatchDeleteTest(BaseTestCase):
    """
    This class is responsible for testing the DELETE feature in sub_batch module
    """

    delete_route_name = "sub-batch.delete"

    def setUp(self):
        """
        This function will run before every test and makes sure required data are ready
        """
        super().setUp()
        self.authenticate()

    def test_success(self):
        """
        Check what happens when valid data is given as input
        """
        sub_batch = baker.make("hubble.SubBatch")
        self.assertDatabaseHas("SubBatch", {"id": sub_batch.id})
        response = self.make_delete_request(
            reverse(self.delete_route_name, args=[sub_batch.id])
        )
        self.assertJSONEqual(
            self.decoded_json(response),
            {"message": "Sub-Batch deleted succcessfully"},
        )
        self.assertDatabaseNotHas("SubBatch", {"id": sub_batch.id})

    def test_failure(self):
        """
        Check what happens when invalid data is given as input
        """
        response = self.make_delete_request(reverse(self.delete_route_name, args=[0]))
        self.assertJSONEqual(
            self.decoded_json(response),
            {"message": "Error while deleting Sub-Batch!"},
        )


class SubBatchDatatableTest(BaseTestCase):
    """
    This class is responsible for testing the Datatables present in the Batch module
    """

    datatable_route_name = "sub-batch-datatable"
    route_name = "batch.detail"

    def setUp(self):
        """
        This function will run before every test and makes sure required data are ready
        """
        super().setUp()
        self.authenticate()
        self.update_valid_input()

    def update_valid_input(self):
        """
        This function is responsible for updating the valid inputs and creating data in databases as reqiured
        """
        self.batch = baker.make("hubble.Batch")
        self.team = baker.make("hubble.Team")
        self.name = self.faker.name()
        self.sub_batch = baker.make(
            "hubble.SubBatch",
            name=seq(self.name),
            team_id=self.team.id,
            batch_id=self.batch.id,
            _quantity=2,
        )
        self.persisted_valid_inputs = {
            "draw": 1,
            "start": 0,
            "length": 10,
            "search[value]": "",
            "batch_id": self.batch.id,
        }

    def test_template(self):
        """
        To makes sure that the correct template is used
        """
        response = self.make_get_request(reverse(self.route_name, args=[self.batch.id]))
        self.assertTemplateUsed(response, "sub_batch/sub_batch.html")
        self.assertContains(response, "SubBatch List")

    def test_datatable(self):
        """
        To check whether all columns are present in datatable and length of rows without any filter
        """
        no_of_teams = (
            Batch.objects.filter(id=self.batch.id)
            .values("sub_batches__team")
            .distinct()
            .count()
        )
        no_of_trainees = (
            Batch.objects.filter(id=self.batch.id)
            .annotate(
                no_of_trainees=Count(
                    "sub_batches__intern_details",
                    filter=Q(sub_batches__intern_details__deleted_at__isnull=True),
                ),
            )
            .values("no_of_trainees")
        )[0]["no_of_trainees"]
        sub_batches = SubBatch.objects.filter(batch=self.batch.id).annotate(
            trainee_count=Count(
                "intern_details",
                filter=Q(intern_details__deleted_at__isnull=True),
            )
        )
        response = self.make_post_request(
            reverse(self.datatable_route_name),
            data=self.get_valid_inputs(),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("extra_data" in response.json())
        self.assertTrue("no_of_teams" in response.json()["extra_data"][0])
        self.assertTrue("no_of_trainees" in response.json()["extra_data"][0])
        self.assertEqual(response.json()["extra_data"][0]["no_of_teams"], no_of_teams)
        self.assertEqual(
            response.json()["extra_data"][0]["no_of_trainees"], no_of_trainees
        )
        for row in range(len(sub_batches)):
            expected_value = sub_batches[row]
            received_value = response.json()["data"][row]
            self.assertEqual(expected_value.pk, int(received_value["pk"]))
            self.assertEqual(expected_value.name, received_value["name"])
            self.assertEqual(
                expected_value.trainee_count,
                int(received_value["trainee_count"]),
            )
            self.assertEqual(expected_value.timeline.name, received_value["timeline"])
            self.assertEqual(
                expected_value.reporting_persons,
                received_value["reporting_persons"],
            )
            self.assertEqual(
                expected_value.start_date.strftime("%d %b %Y"),
                received_value["start_date"],
            )
        for row in response.json()["data"]:
            self.assertTrue("pk" in row)
            self.assertTrue("name" in row)
            self.assertTrue("team" in row)
            self.assertTrue("trainee_count" in row)
            self.assertTrue("reporting_persons" in row)
            self.assertTrue("timeline" in row)
            self.assertTrue("start_date" in row)
            self.assertTrue("action" in row)
        self.assertTrue(response.json()["recordsTotal"], len(self.sub_batch))

    def test_datatable_search(self):
        """
        To check what happens when search value is given
        """
        name_to_be_searched = self.name + "1"
        response = self.make_post_request(
            reverse(self.datatable_route_name),
            data=self.get_valid_inputs({"search[value]": name_to_be_searched}),
        )
        self.assertTrue(
            response.json()["recordsTotal"],
            SubBatch.objects.filter(name__icontains=name_to_be_searched).count(),
        )
