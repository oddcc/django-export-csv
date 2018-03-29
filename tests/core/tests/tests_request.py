from __future__ import unicode_literals
from __future__ import absolute_import
from django.test import TestCase


class ResponseTests(TestCase):
    def test_cbv_export(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header("Content-Disposition"))
        self.assertEqual(response['Content-Type'], 'text/csv')

        response = self.client.get('/college')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header("Content-Disposition"))
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_fbc_export(self):
        response = self.client.get('/function')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header("Content-Disposition"))
        self.assertEqual(response['Content-Type'], 'text/csv')
