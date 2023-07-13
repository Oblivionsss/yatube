import pytest

from django.core.paginator import Paginator, Page


class TestGroupPaginatorView:

	@pytest.mark.django_db(transaction=True)
	def test_group_paginator_view_get(self, client, post_with_group):
		try:
			response = client.get(f'/group/{post_with_group.group.slug}')
		except Exception as e:
			assert False, f'''неправильно работает страница /group/slug, ошибка {e}'''
		if response.status_code in (301, 302):
			response = client.get(f'/group/{post_with_group.group.slug}')
		assert response.status_code != 404, \
			f'''Страница `/group/<slug>/` не найдена, проверьте этот адрес в *urls.py*'''

		assert 'paginator' in response.context, \
			f'''Проверьте, что передали переменную `paginator` в контекст страницы `/group/<slug>/`'''
		assert type(response.context['paginator']) == Paginator, \
			f'''Проверьте, что переменная `paginator` является типом `paginator`''' 
		assert 'page' in response.context, \
			f'''Проверьте, что передали переменную `page` в контекст страницы `/group/<slug>/`'''
		assert type(response.context['page']) == Page, \
			f'''Проверьте, что переменная `page` является типом `page`'''

	@pytest.mark.django_db(transaction=True)
	def test_index_paginator_view_get(self, client, post_with_group):
		try:
			response = client.get(f'/')
		except Exception:
			assert False, f'''неправильно работает начальная страница `/`, ошибка {e}'''
		assert response.status_code != 404, \
			f'''Стартовая страница `/` не найдена, проверьте этот адрес в *urls.py*'''

		assert 'paginator' in response.context, \
			f'''Проверьте, что передали переменную `paginator` в контекст страницы `/group/<slug>/`'''
		assert type(response.context['paginator']) == Paginator, \
			f'''Проверьте, что переменная `paginator` является типом `paginator`''' 
		assert 'page' in response.context, \
			f'''Проверьте, что передали переменную `page` в контекст страницы `/group/<slug>/`'''
		assert type(response.context['page']) == Page, \
			f'''Проверьте, что переменная `page` является типом `page`'''

