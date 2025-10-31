from django.test import TestCase


class DashboardAuthRedirectTests(TestCase):
    def test_dashboard_requires_authentication(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
