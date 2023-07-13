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
		assert len(response.context['form'].fields) == 2, \
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


	def test_new_view_post(self, user_client):
		pass