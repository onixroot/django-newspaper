from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client

from .models import *

# Create your tests here.

class CommentTests(TestCase):
	
	def setUp(self):
		self.client = Client()
		self.user = get_user_model().objects.create_user(username="testuser", password="testpassword123")
		self.category = Category.objects.create(name='testcategory')
		self.article = Article.objects.create(title='testtitle', body='testbody', category=self.category, author=self.user)
		
	def test_comment_new(self):
		self.client.login(username='testuser', password='testpassword123')
		response = self.client.post(f'/articles/{self.article.pk}/comment_new', {'comment': "testcomment"})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Comment.objects.last().comment, "testcomment")
		self.assertEqual(Comment.objects.last().author, self.user)
		self.assertEqual(Comment.objects.last().article, self.article)