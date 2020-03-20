from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):
	def test_home_page_status_code(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)


class SignupPageTests(TestCase):
	username = 'newuser'
	email = 'newuser@email.com'

	def test_signup_form(self):
		new_user = get_user_model().objects.create_user(self.username, self.email)
		self.assertEqual(get_user_model().objects.all().count(), 1)
		self.assertEqual(get_user_model().objects.all()[0].username, self.username)
		self.assertEqual(get_user_model().objects.all()[0].email, self.email)