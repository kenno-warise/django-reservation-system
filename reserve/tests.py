from django.test import TestCase
from django.urls import reverse


class IndexTests(TestCase):
    def test_index_display(self):
        """
        予約画面
        """
        response = self.client.get(reverse("reserve:index"))
        self.assertEqual(response.status_code, 200)

# Create your tests here.
