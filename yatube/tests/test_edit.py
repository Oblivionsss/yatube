import pytest

from django import forms
from posts.models import Post
from django.test import Client

class TestEdit:
	# Проверка создания страницы (profile) при регистрации
	@pytest.mark.django_db(transaction=True)
	def test_new_page_profile(self, user_client):
		try:
			response = user_client.get('/TestUser')
		except Exception as e:
			assert False, f'''Страница созданного пользователя TestCase работает неправильно. Ошибка: `{e}`'''
		if response.status_code == 200:
			response = user_client.get('/TestUser')
		assert response.status_code != 404, 'Страница `/TestUser/` не найдена, проверьте этот адрес в *urls.py*'
	
	# проверка создания поста авторизованным пользователем
	@pytest.mark.django_db(transaction=True)
	def test_new_view_post(self, user_client, user, group):
		text = 'Проверка нового поста!'
		try:
			response = user_client.get('/new')
		except Exception as e:
			assert False, f'''Страница `/new` работает неправильно. Ошибка: `{e}`'''
		url = '/new/' if response.status_code in (301, 302) else '/new'

		response = user_client.post(url, data={'text': text, 'group': group.id})

		assert response.status_code in (301, 302), \
			'Проверьте, что со страницы `/new/` после создания поста перенаправляете на главную страницу'
		post = Post.objects.filter(author=user, text=text, group=group).first()
		assert post is not None, 'Проверьте, что вы сохранили новый пост при отправки формы на странице `/new/`'
		assert response.url == '/', 'Проверьте, что перенаправляете на главную страницу `/`'

		text = 'Проверка нового поста 2!'
		response = user_client.post(url, data={'text': text})
		assert response.status_code in (301, 302), \
			'Проверьте, что со страницы `/new/` после создания поста перенаправляете на главную страницу'
		post = Post.objects.filter(author=user, text=text, group__isnull=True).first()
		assert post is not None, 'Проверьте, что вы сохранили новый пост при отправки формы на странице `/new/`'
		assert response.url == '/', 'Проверьте, что перенаправляете на главную страницу `/`'

		response = user_client.post(url)
		assert response.status_code == 200, \
			'Проверьте, что на странице `/new/` выводите ошибки при неправильной заполненной формы `form`'

	# Проверка невозможности публикования поста неавторизованному пользователю 
	@pytest.mark.django_db(transaction=True)
	def test_new_view_post_not_auth(self):
		client = Client()
		try:
			response = client.get('/new')
		except Exception as e:
			assert False, f'''Страница `/new` работает неправильно. Ошибка: `{e}`'''
		assert response.status_code in (301, 302), \
			'Проверьте, что при обращении на страницу `/new/` неавт. польз. перенаправляете страницу регистрации'

	# После публикации поста новая запись появляется на главной странице сайта (index), 
	# на персональной странице пользователя (profile), и на отдельной странице поста (post) 
	@pytest.mark.django_db(transaction=True)
	def test_new_view_post(self, user_client, user, group):
		text = 'Проверка нового поста!'
		try:
			response = user_client.get('/new')
		except Exception as e:
			assert False, f'''Страница `/new` работает неправильно. Ошибка: `{e}`'''
		url = '/new/' if response.status_code in (301, 302) else '/new'

		response = user_client.post(url, data={'text': text, 'group': group.id})

		assert response.status_code in (301, 302), \
			'Проверьте, что со страницы `/new/` после создания поста перенаправляете на главную страницу'
		post = Post.objects.filter(author=user, text=text, group=group).first()
		assert post is not None, 'Проверьте, что вы сохранили новый пост при отправки формы на странице `/new/`'
		assert response.url == '/', 'Проверьте, что перенаправляете на главную страницу `/`'

		# проверка отображения на главной странице
		response = user_client.get('')
		assert response.status_code != 404, \
			'Страница index не найдена, проверьте этот адрес в *urls.py*'
		
