import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


# Create your tests here.


class TestLabel(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user", password="test_user", email='username="test@user.com"'
        )
        self.client.force_authenticate(user=self.user)

    def test_post_label(self):
        post_data = dict(name="Benign")
        create_response = self.client.post(
            path=reverse("label-list"),
            content_type="application/json",
            data=json.dumps(post_data),
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        post_data = dict(name="Malignant")
        create_response = self.client.post(
            path=reverse("label-list"),
            content_type="application/json",
            data=json.dumps(post_data),
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
