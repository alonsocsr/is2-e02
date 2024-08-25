from django.urls import reverse
from django.test import TestCase


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse("home")

    def test_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
