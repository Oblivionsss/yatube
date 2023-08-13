import pytest

from django.contrib.auth.models import User
from django.core.cache import cache

from posts.models import Follow, Post


class TestComment:
    @pytest.mark.django_db(transaction=True) 
    def test_comment_auth_user(self, client):
        cache.clear()
        author = User.objects.create(username='sarah_conor',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)

		# Пользователь, на которого будем подисываться, user2
        commentator = User.objects.create(username='john_wick',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)

        client.force_login(commentator)

        post = Post.objects.create(text='Тестовый пост_1', author=author)

        # проверка пост создан
        try:
            response = client.get(f'/{author.username}/{post.id}')
        except Exception as e:
            assert False, \
            f'''Страница подписки /username/follow/ работает неправильно, проверьте её корректность, ошибка {e}'''
        if response.status_code in (301, 302):
            response = client.get(f'/{author.username}/{post.id}/')
        assert response.status_code != 404, \
            f'''Страница /username/follow/ не найдена, проверьте корректность файла url'''
        
        
        # создаем комментарий 
        url = f'/{author.username}/{post.id}'
        response = client.post(url, data={
                        'text': 'Пробный комментарий!',
                    }
        )
        # assert response.status_code == 200 and response.url.startswith(f'/{author.username}/{post.id}'), \
        #     f'''Проверьте что комментарий добавляется к посту {response}'''
