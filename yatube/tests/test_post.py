import pytest

from django.core.paginator import Paginator, Page

from django import forms
from posts.models import Post
from django.contrib.auth import get_user_model


def get_field_context(context, field_type):
	for field in context.keys():
		if field not in ('user', 'request') and type(context[field]) == field_type:
			return context[field]
	return None

class TestPostView:

	# Проверка доступности поста для просмотра `/username/post_id`
	@pytest.mark.django_db(transaction=True)
	def test_post_edit_auth(self, user, client, post_with_group):
		try:
			response = client.get(f'/{post_with_group.author.username}/{post_with_group.id}')
		except Exception as e:
			assert False, f'''Страница `/username/<post_id>/` работает неправильно, ошибка {e}'''
		if response.status_code in (301, 302):
			response = client.get(f'/{post_with_group.author.username}/{post_with_group.id}/')
		assert response.status_code != 404, \
			f'''Проверьте корректность адреса и доступ для username к посту `/username/<post_id>/`'''

		profile_context = get_field_context(response.context, get_user_model())
		assert profile_context is not None, \
			f'''Проверьте, что передали автора в контекст страницы `/<username>/<post_id>/`'''

		post_context = get_field_context(response.context, Post)
		assert post_context is not None, \
			f'''Проверьте, что передали статью в контекст страницы `/<username>/<post_id>/`'''


class PostEditView:

	# Проверка доступности поста для редактирования 
	@pytest.mark.django_db(transaction=True)
	def test_post_edit_view_author_get(self, client, post_with_group):
		try:
			response = client.get(f'/{post_with_group.author.username}/{post_with_group.id}/edit')
		except Exception as e:
			assert False, f'''Страница `/username/<post_id>/edit` работает неправильно, ошибка {e}'''
		if response.status_code in (301, 302) and not response.url.startswith(f'/{post_with_group.author.username}/{post_with_group.id}'):
			response = client.get(f'/{post_with_group.author.username}/{post_with_group.id}/edit/')
		assert response.status_code != 404, \
			f'''Проверьте корректность адреса и доступ для username к посту `/username/<post_id>/edit`'''

		post_context = get_field_context(response.context, Post)
		assert post_context is not None, \
			f'''Проверьте, что передали статью в контекст страницы `/<username>/<post_id>/`'''

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