from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase


class ApiHealthTests(TestCase):
    def test_health_endpoint_returns_json(self):
        response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_health_endpoint_only_accepts_get(self):
        response = self.client.post("/api/health/")

        self.assertEqual(response.status_code, 405)

    def test_homepage_remains_available(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "server run like new")


class StudentsApiTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="student-api-user",
            password="test-password-123",
        )

    def test_docs_and_schema_are_public(self):
        docs_response = self.client.get("/api/docs/")
        schema_response = self.client.get("/api/schema/")

        self.assertEqual(docs_response.status_code, 200)
        self.assertEqual(schema_response.status_code, 200)
        self.assertIn("/api/students/", schema_response.json()["paths"])

    def test_student_crud_requires_token_authentication(self):
        response = self.client.get("/api/students/")
        self.assertEqual(response.status_code, 401)

        token_response = self.client.post(
            "/api/token/",
            {"username": "student-api-user", "password": "test-password-123"},
        )
        self.assertEqual(token_response.status_code, 200)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token_response.data['token']}"
        )

        create_response = self.client.post(
            "/api/students/",
            {"name": "Ada Student", "email": "ada@example.com", "age": 20},
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        student_id = create_response.data["id"]

        list_response = self.client.get("/api/students/")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data), 1)

        detail_response = self.client.get(f"/api/students/{student_id}/")
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.data["name"], "Ada Student")

        update_response = self.client.patch(
            f"/api/students/{student_id}/",
            {"age": 21},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data["age"], 21)

        delete_response = self.client.delete(f"/api/students/{student_id}/")
        self.assertEqual(delete_response.status_code, 204)
