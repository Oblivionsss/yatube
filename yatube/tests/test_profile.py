import pytest

from django.core.paginator import Paginator, Page
from django.contrib.auth import get_user_model


def search_fields(context, field_type):
    for field in context.keys():
        if field not in ('user', 'request') and type(context[field]) == field_type:
            return context[field]
    return None

class TestProfileView:
    # Проверка передачи author и его статей в context
    @pytest.mark.django_db(transaction=True)
    def test_profile_view_get(self, post_with_group, client):
        try:
            response = client.get(f'/{post_with_group.author.username}')
        except Exception as e:
            assert False, \
            f'''Страница /username/ работает неправильно!, ошибка {e}'''
        if response.status_code in (301, 302):
            response = client.get(f'/{post_with_group.author.username}/')
        assert response.status_code != 404, \
            f'''Страница `/<username>/` не найдена, проверьте этот адрес в *urls.py*'''

        author_context = search_fields(response.context, get_user_model())
        assert author_context is not None, \
            f'''Проверьте, что вы передали автора в контекст страницы /username/'''
        
        page_context = search_fields(response.context, Page)
        assert page_context is not None, \
            f'''Проверьте, что вы передали page в контекст страницы /username/'''
        # уже создана одна запись
        assert len(page_context.object_list) == 1, \
            f'''Проверьте, что вы передали статьи в контекст страницы /username/'''
        
        paginator_context = search_fields(response.context, Paginator)
        assert paginator_context is not None, \
            f'''Проверьте, что вы передали paginator в контекст страницы /username/'''
        
        new_user = get_user_model()(username='new_user_98')
        new_user.save()
        try:
            response = client.get(f'/{new_user.username}')
        except Exception as e:
            assert False, \
            f'''Страница /username/ работает неправильно!, ошибка {e}'''
        if response.status_code in (301, 302):
            response = client.get(f'/{new_user.username}/')
        
        page_context = search_fields(response.context, Page)
        assert page_context is not None, \
            f'''Проверьте, что вы передали page в контекст страницы /username/'''
        # записей у автора new_user не существует
        assert len(page_context.object_list) == 0, \
            f'''Проверьте, что вы передали статьи в контекст страницы /username/'''

        