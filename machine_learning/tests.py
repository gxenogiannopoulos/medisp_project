import json
import os

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from medisp_project.settings import HIST_IMAGES


# Create your tests here.


class TestLabel(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user", password="test_user", email='username="test@user.com"'
        )
        self.client.force_authenticate(user=self.user)

    def test_post_labels(self):
        new_label_name = "Benign"
        post_data = dict(name=new_label_name)
        create_response = self.client.post(
            path=reverse("labels-list"),
            content_type="application/json",
            data=json.dumps(post_data),
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            create_response.data, create_response.data | {"name": new_label_name}
        )

        MALIGNANT = "Malignant"
        post_data = dict(name=MALIGNANT)
        create_response = self.client.post(path=reverse("labels-list"), data=post_data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            create_response.data, create_response.data | {"name": MALIGNANT}
        )


class TestHistImageModelViewset(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user", password="test_user", email="test@user.com"
        )
        self.client.force_authenticate(user=self.user)

    def test_register_images(self):
        expected_response = [
            file for file in os.listdir(os.path.join(HIST_IMAGES, "train"))
        ]
        response = self.client.post(reverse("hist-images-register-images"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
