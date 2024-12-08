from datetime import date

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from task_app.models import userReg, Task

class UserRegModelTest(TestCase):

    def setUp(self):
        self.user = userReg.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@me.com",
            age=30,
            gender="Male"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertEqual(self.user.email, "testuser@me.com")
        self.assertEqual(self.user.age, 30)
        self.assertEqual(self.user.gender, "Male")


class TaskModelTest(TestCase):

    def setUp(self):
        self.user = userReg.objects.create_user(
            username="taskuser",
            password="taskpassword"
        )
        self.task = Task.objects.create(
            user=self.user,
            task_name="Sample Task",
            description="This is a test task.",
            due_date=date(2024, 12, 31),
            status="Pending"
        )

    def test_task_creation(self):
        self.assertEqual(self.task.task_name, "Sample Task")
        self.assertEqual(self.task.description, "This is a test task.")
        self.assertEqual(self.task.due_date, date(2024, 12, 31))
        self.assertEqual(self.task.status, "Pending")
        self.assertTrue(self.task.is_active)







class UserViewSetTest(APITestCase):

    def setUp(self):
        self.user = userReg.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.login_url = "/api/login/"
        self.signup_url = "/api/create/"

    def test_user_registration(self):
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
            "age": 25,
            "gender": "Female"
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Record Saved successfully")

    def test_user_login(self):
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], self.user.id)
        
        self.assertIn("token", response.data)


class TaskViewSetTest(APITestCase):

    def setUp(self):
        self.user = userReg.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.task_url = "/api/tasks/"
        self.task_url_without_slash = "/api/tasks/"
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        
        Task.objects.create(
            user=self.user,
            task_name="Task 1",
            due_date=date(2024, 12, 31),
            status="Pending"
        )
        Task.objects.create(
            user=self.user,
            task_name="Task 2",
            due_date=date(2024, 12, 31),
            status="Completed"
        )

    def test_task_creation(self):
        data = {
            "task_name": "New Task",
            "description": "This is a new task",
            "due_date": "2024-12-31",
            "user": self.user.id,
        }
        response = self.client.post(self.task_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["task_name"], "New Task")

    def test_get_all_tasks(self):
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        
    def test_get_tasks_with_filter(self):
        response = self.client.get(self.task_url_without_slash + '?status=Pending')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_tasks_with_pagination(self):
        response = self.client.get(self.task_url_without_slash + '?page=1&page_size=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        
    def test_task_update(self):
        task = Task.objects.create(
            user=self.user,
            task_name="Task to Update",
            due_date=date(2024, 12, 31),
            status="Pending"
        )
        url = f"{self.task_url}{task.id}/"
        data = {"status": "Completed"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, "Completed")

    def test_task_deletion(self):
        task = Task.objects.create(
            user=self.user,
            task_name="Task to Delete",
            due_date=date(2024, 12, 31),
            status="Pending"
        )
        url = f"{self.task_url}{task.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertFalse(task.is_active)
