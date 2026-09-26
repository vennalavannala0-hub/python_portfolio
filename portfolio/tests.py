from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, SiteProfile


class PortfolioSiteTests(TestCase):
    def test_home_renders_seeded_profile(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        profile = SiteProfile.objects.first()
        self.assertIsNotNone(profile)
        self.assertContains(response, profile.full_name)
        self.assertContains(response, "View Projects")
        self.assertContains(response, "Contact Me")

    def test_robots_and_sitemap(self):
        self.assertEqual(self.client.get("/robots.txt").status_code, 200)
        self.assertEqual(self.client.get("/sitemap.xml").status_code, 200)

    def test_contact_form_rejects_short_message(self):
        response = self.client.post(
            reverse("home"),
            {"name": "Ada", "email": "ada@example.com", "message": "Hi"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(response, "at least 12 characters")

    def test_contact_form_saves_valid_message(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "message": "I would like to discuss a Django API project.",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertContains(response, "Thanks for the message")
