import json

from django.test import TestCase


class SendMessageAPITestCase(TestCase):
    def setUp(self):
        # Set up any necessary data or configurations for the test
        self.url = "http://127.0.0.1:8000/api/send-message/"
        self.valid_payload = {
            "user_id": "test2201",
            "sender": "123456789",
            "receiver": "987654321",
            "content": "What is my name?"
        }

    def test_send_message_success(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_send_message_missing_field(self):
        invalid_payload = {
            "user_id": "test2201",
            "sender": "123456789",
            # Missing 'receiver' and 'content'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
