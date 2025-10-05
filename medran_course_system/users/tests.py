from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class RegistrationTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.url = reverse('register')

	def test_register_with_label_role(self):
		payload = {
			'username': 'label_user',
			'email': 'label@example.com',
			'password': 'testpass123',
			'role': 'Student'
		}
		resp = self.client.post(self.url, payload, content_type='application/json')
		self.assertEqual(resp.status_code, 200)
		User = get_user_model()
		self.assertTrue(User.objects.filter(username='label_user').exists())

	def test_register_with_key_role(self):
		payload = {
			'username': 'key_user',
			'email': 'key@example.com',
			'password': 'testpass123',
			'role': 'student'
		}
		resp = self.client.post(self.url, payload, content_type='application/json')
		self.assertEqual(resp.status_code, 200)
		User = get_user_model()
		self.assertTrue(User.objects.filter(username='key_user').exists())

