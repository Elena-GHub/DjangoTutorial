from django.test import TestCase

from django.urls import reverse


class CommonHomeViewTests(TestCase):
    def test_welcome_message_displayed(self):
        """
        Welcome message is displayed in website home page.
        """
        response = self.client.get(reverse('common:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to my Learning Django playground!")
