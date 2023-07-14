import pytest

from django import forms
from posts.models import Post

class TestPostEdit:

	@pytest.mark.django_db(transaction=True)
	def test_post_edit_auth(self, user, post_with_group):
		try:
			response = client.get(f'/{post_with_group.author.username}')
		except Exception:
			assert False, \
			f'''Страница /username/ работает неправильно!, ошибка {e}'''
		if response.status_code in (301, 302):
			response = client.get(f'/{post_with_group.author.username}/')
		assert response.status_code != 404, \
			f'''Страница `/<username>/` не найдена, проверьте этот адрес в *urls.py*'''

		# Проверка созданного поста по умолчанию
		post = Post.objects.filter(author=user, text=post_with_group.text, group=post_with_group.group)
		assert Post.objects.all().count() == 1, \
			f'''Проверьте, что вы создали запись'''

		url = f'''/{post_with_group.author.username}/{post_with_group.pk}'''
		
		# Проверка доступа автора к посту
		try:
			response = client.get(url)
		except Exception as e:
			assert False, f '''Страница `/username/post_id/` работает неправильно, ошибка {e}'''
		if response.status_code in (301, 302):
			response = client.get(f'/{post_with_group.author.username}/{post_with_group.pk}/')
		assert response.status_code != 404, \
			f'''Проверьте корректность адреса и доступ для username к посту `/username/post_id/`'''
