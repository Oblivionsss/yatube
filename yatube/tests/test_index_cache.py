from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.cache import cache

from posts.models import Post, Group
from django.urls import reverse


class TestCacheIndexView(TestCase):
	"""
	Проверка кэширования главной страницы `/`.
	"""
	def setUp(self):
		cache.clear()

		self.client = Client()
		self.user = User.objects.create_user(
	 		username='sarah_conor',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)
		self.client.force_login(self.user)

		self.group = Group.objects.create(
			title='Тестовая группа 1', 
			slug='test-link', 
			description='Тестовое описание группы'
		)

		self.post = Post.objects.create(
			text='Тестовый пост',
			author=self.user,
			group=self.group,
		)

		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.post.text)

	def test_cache_imndex_get(self):

		self.post_cached = Post.objects.create(
			text='Тестовый пост 2',
			author=self.user,
			group=self.group,
		)

		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.post.text)
		self.assertNotContains(response, self.post_cached.text)
