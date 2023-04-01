import json
import os

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from machine_learning.models import Label, HistImage
from machine_learning.serializers import HistImageSerializer
from medisp_project.settings import HIST_IMAGES


# Create your tests here.


class TestLabel(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.existing_label = Label.objects.create(name="label_init")
        cls.label_to_delete = Label.objects.create(name="label_to_delete")

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user", password="test_user", email='username="test@user.com"'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_label(self):
        response = self.client.get(
            path=reverse("labels-list"),
            data={"pk": self.existing_label.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.existing_label.name)

    def test_create_label(self):
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

    def test_update_label(self):
        response = self.client.put(
            path=reverse(
                "labels-detail",
            ),
            data={"name": "label_updated"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_label = Label.objects.get(pk=self.existing_label.pk)
        self.assertEqual(updated_label.name, "label_updated")

    def test_delete_label(self):
        response = self.client.delete(
            path=reverse(
                "labels-detail",
            ),
            kwargs={"pk": self.label_to_delete.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Label.objects.filter(pk=self.label_to_delete.pk).exists())


class TestHistImageModelViewset(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user", password="test_user", email="test@user.com"
        )
        self.client.force_authenticate(user=self.user)

    def test_register_images(self):
        dataset_folder = os.path.join(HIST_IMAGES, "train")
        # Prepare labels
        labels = Label.objects.bulk_create(
            [
                Label(name=name)
                for name in [folder_name for folder_name in os.listdir(dataset_folder)]
            ]
        )
        id_counter = 1
        hist_images = []
        for label in labels:
            image_folder = os.path.join(dataset_folder, label.name)
            for image_filename in os.listdir(image_folder):
                image_filepath = os.path.join(image_folder, image_filename)
                hist_images.append(
                    HistImage(id=id_counter, label=label, file=image_filepath)
                )
                id_counter += 1
        expected_response = HistImageSerializer(hist_images, many=True).data
        response = self.client.post(reverse("hist-images-register-images"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
