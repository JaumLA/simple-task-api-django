import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from tasks.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestTaskAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.url = reverse("task-list")

    def test_create_task(self):
        payload = {"description": "Test", "init_time": "1:00", "end_time": "2:00"}
        response = self.client.post(self.url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        task_id = response.data["id"]

        from tasks.models import Task
        task_no_banco = Task.objects.get(id=task_id)
        assert task_no_banco.user == self.user
        assert task_no_banco.description == payload["description"]

    def test_failure_inverse_time(self):
        payload = {"description": "Test Task", "init_time": "2:00", "end_time": "1:00"}
        response = self.client.post(self.url, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        print(response)
        assert "End time must be greater than init time." in response.data['end_time']