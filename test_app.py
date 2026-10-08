import unittest

from app import app


class MonitoringPlatformTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint(self):
        response = self.client.get("/healthz")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["status"], "healthy")

    def test_metrics_endpoint(self):
        response = self.client.get("/metrics")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIn("cpu_usage_percent", data)
        self.assertIn("memory_usage_percent", data)
        self.assertIn("uptime_seconds", data)
        self.assertIn("request_count", data)


if __name__ == "__main__":
    unittest.main()