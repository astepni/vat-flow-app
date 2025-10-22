from django.test import TestCase


class LandingPageTestCase(TestCase):
    def test_check_if_landing_page_is_reachable_when_user_not_authed(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "landing.html")
        self.assertEqual(response.status_code, 200)

    def test_check_if_landing_page_is_reachable_when_user_authed(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "landing.html")
        self.assertEqual(response.status_code, 200)
