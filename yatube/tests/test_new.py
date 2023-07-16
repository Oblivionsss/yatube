import pytest

from django import forms
from posts.models import Post

class TestNew:

	# Проверка отображения страницы создания записи
	def test_new_view_get(self, user_client):
		try:
			response = user_client.get('/new')
		except Exception as e:
			assert False, \
			f'''Страница /new/ работает неправильно, проверьте её корректность, ошибка {e}'''
		if response.status_code in (301, 302):
			response = user_client.get('/new/')
		assert response.status_code != 404, \
			f'''Страница /new не найдена, проверьте корректность файла url'''

		assert 'form' in response.context, \
			f'''Проверьте, что вы передали `form` в контекст'''
		assert len(response.context['form'].fields) == 3, \
			f'''Проверьте корректность form, в нем должно быть 2 field'''
		assert 'group' in response.context['form'].fields, \
			f'''Проверьте, что поле `group` добавлено в `form`'''
		assert type(response.context['form'].fields['group']) == forms.models.ModelChoiceField, \
			f'''Проверьте, что в форме `form` на странице `/new/` поле `group` типа `ModelChoiceField`'''
		assert not response.context['form'].fields['group'].required, \
			f'''Проверьте, что в форме `form` на странице `/new/` поле `group` не обязательно'''

		assert 'text' in response.context['form'].fields, \
			f'''Проверьте, что поле `text` добавлено в `form`'''
		assert type(response.context['form'].fields['text']) == forms.fields.CharField, \
			f'''Проверьте, что в форме `form` на странице `/new/` поле `text` типа `CharField`'''
		assert response.context['form'].fields['text'].required, \
			f'''Проверьте, что в форме `form` на странице `/new/` поле `text` не обязательно'''

		assert 'image' in response.context['form'].fields, \
			f'''Проверьте, что поле image добавлеон в form'''
		assert type(response.context['form'].fields['image']) == forms.fields.ImageField, \
			f'''Проверьте, что в форме `form` на странице `/new/` поле `image` типа `ImageField`'''

	def test_new_view_post(self, user_client, user, group):
		# Проверка создания поста
		text1 = "Проверка нового поста 1"
		try:
			response = user_client.get('/new')
		except Exception as e:
			assert False, \
			f'''Страница /new/ работает неправильно, проверьте её корректность, ошибка {e}'''
		if response.status_code in (301, 302):
			response = user_client.get('/new/')
		url = '/new/' if response.status_code in (301, 302) else '/new'
		
		response = user_client.post(url, data={'text': text1, 'group': group.id})
		
		assert response.status_code in (301, 302), \
			f'''Проверьте, что после создания поста Вы перенаправляетесь на стартовую страницу`/`'''
		post = Post.objects.filter(author=user, text=text1, group=group.id).first()
		assert post is not None, \
			f'''Проверьте, что вы сохранили новый пост при отправки формы на странице `/new/`'''
		assert response.url == '/', \
			f'''Проверьте, что после создания поста Вы перенаправляется на стартовую страницу `/`'''

		# Проверка создания поста без обязательного поля `group`
		text2 = "Проверка второго поста"
		response = user_client.post(url, data={'text': text1, })
		assert response.status_code in (301, 302), \
			f'''Проверьте, что после создания поста без группы Вы перенаправляетесь на стартовую страницу `/`'''
		post = Post.objects.filter(author=user, text=text1, group__isnull=True).first()
		assert post is not None, \
			f'''Проверьте, что вы сохранили новый пост при отправки формы на странице `/new/`'''
		assert response.url == '/', \
			f'''Проверьте, что после создания поста Вы перенаправляется на стартовую страницу `/`'''

		# Проверка создания поста без данных, и отсутствие вызова ошибок
		response = user_client.post(url)
		assert response.status_code == 200, \
			f'''Проверьте, что при некорректном создании поста Вы возвращаетсь на `/new` с указанием на ошибки'''