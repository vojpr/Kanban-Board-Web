from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from kanban_app.models import Task
import json


class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_credentials = {"username": "created_user", "password": "createdpass123"}
        cls.created_user = User.objects.create_user(
            username=cls.user_credentials["username"], 
            password=cls.user_credentials["password"],
        )


class IndexPageViewTest(TestCase):
    def test_view_by_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "index.html")


class BoardViewTest(BaseTest):
    def test_view_by_url(self):
        self.client.login(username=self.user_credentials["username"], password=self.user_credentials["password"])
        response = self.client.get("/board/")
        self.assertEqual(response.status_code, 200)

    def test_view_by_name(self):
        self.client.login(username=self.user_credentials["username"], password=self.user_credentials["password"])
        response = self.client.get(reverse("board"))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        self.client.login(username=self.user_credentials["username"], password=self.user_credentials["password"])
        response = self.client.get(reverse("board"))
        self.assertTemplateUsed(response, "kanban_app/board.html")

    def test_list_only_users_tasks(self):
        self.client.login(username=self.user_credentials["username"], password=self.user_credentials["password"])
        response = self.client.get(reverse("board"))
        users_query_set = response.context["tasks"].order_by("user").values("user").distinct()
        self.assertEqual(users_query_set.count(), 1)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("board"))
        self.assertRedirects(response, "/?next=/board/", status_code=302, target_status_code=200, fetch_redirect_response=True)


class CreateTaskTest(BaseTest):
    def test_view_by_url(self):
        self.client.login(username=self.user_credentials["username"], password=self.user_credentials["password"])
        response = self.client.get("/create/", data={"new-task": "new test task"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(task_text="new test task").exists())
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"status": "success", "task": {"text": "new test task", "pk": 5}}
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get("/create/")
        self.assertRedirects(response, "/?next=/create/", status_code=302, target_status_code=200, fetch_redirect_response=True)


class DeleteTaskTest(BaseTest):
    def test_view_by_url(self):
        self.client.login(username=self.user_credentials["username"], password=self.user_credentials["password"])
        self.client.get("/create/", data={"new-task": "new test task"})
        response = self.client.get("/delete/", data={"pk": 5})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(task_text="new test task").exists())
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"status": "success", "deleted": True}
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get("/delete/")
        self.assertRedirects(response, "/?next=/delete/", status_code=302, target_status_code=200, fetch_redirect_response=True)


class ReorderTaskTest(BaseTest):
    def test_view_by_url(self):
        self.client.login(username=self.user_credentials["username"], password=self.user_credentials["password"])
        response = self.client.get(
            "/reorder/",
            data={
                "sort": json.dumps(
                    [
                        {"pk": 1, "order": 0, "column_name": "To-do"},
                        {"pk": 2, "order": 1, "column_name": "To-do"},
                        {"pk": 3, "order": 0, "column_name": "In progress"},
                        {"pk": 4, "order": 0, "column_name": "Done"},
                    ]
                )
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {"status": "success", "reordered": True}
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get("/reorder/")
        self.assertRedirects(response, "/?next=/reorder/", status_code=302, target_status_code=200, fetch_redirect_response=True)
