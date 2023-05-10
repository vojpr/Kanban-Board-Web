from django.test import TestCase
from django.contrib.auth.models import User
from kanban_app.models import Task
import pytz
from unittest import mock
import datetime


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.created_user = User.objects.create_user(username="created_user", password="createdpass123")

    def create_new_task(self, task_text="New task"):
        return Task.objects.create(user=self.created_user, column_name="To-do", task_text=task_text)

    def test_create_default_tasks_signal(self):
        users_task_list = Task.objects.filter(user=self.created_user).all()
        self.assertEqual(users_task_list.count(), 4)
    
    def test_new_task_creation(self):
        new_task = self.create_new_task()
        self.assertTrue(isinstance(new_task, Task))
        self.assertEqual(new_task.task_text, "New task")
        self.assertEqual(new_task.order, 0)
        self.assertEqual(new_task.__str__(), f"{new_task.user}'s board - {new_task.column_name} column - Task {new_task.pk}")
        users_task_list = Task.objects.filter(user=self.created_user).all()
        self.assertEqual(users_task_list.count(), 5)

    def test_created_at_date(self):
        mocked = datetime.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            new_task = self.create_new_task()
            self.assertEqual(new_task.created_at, mocked)
