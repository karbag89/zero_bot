from flask import url_for

from tests.base import BaseTestCase


class TestAdminPanel(BaseTestCase):
    def test_signin(self):
        self.assertEqual(self.client.get(url_for(endpoint="signin")).status_code, 200)

    def test_admin(self):
        self.assertEqual(self.client.get(url_for(endpoint="admin")).status_code, 200)

    def test_statistics(self):
        self.assertEqual(self.client.get(url_for(endpoint="statistics")).status_code, 200)