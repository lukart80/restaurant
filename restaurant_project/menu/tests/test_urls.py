from django.test import TestCase, Client


class TestMenu(TestCase):
    HOMEPAGE_URL = '/'

    def setUp(self):
        self.anonymous_client = Client()

    def test_menu_urls(self):
        url_code = {
            self.HOMEPAGE_URL: 200,
        }
        for url, code in url_code.items():
            with self.subTest(url=url):
                response = self.anonymous_client.get(url)
                self.assertEqual(response.status_code, code)
