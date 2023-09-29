import pytest

from django.contrib.auth.models import User
from django.core.cache import cache

from posts.models import Follow, Post, Comment


class TestComment:
    """
    Проверка добавления комментария.
    
        Варианты
        # 1. Пользователь1 создает пост 
        # 2. Пользователь2 добавляет комментарий
        # 3. Неавторизованный пользователь не имеет возможности добавить комментарий
        # 4.

    
    """
    @pytest.mark.django_db(transaction=True) 
    def test_comment_auth_user(self, client):
        
        # 1
        cache.clear()
        create_post_author = User.objects.create(username='sarah_conor',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)

        commentator_post = User.objects.create(username='john_wick',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)

        client.force_login(commentator_post)
        post = Post.objects.create(text='Тестовый пост_1', author=create_post_author)

        # проверка создания поста
        try:
            response = client.get(f'/{create_post_author.username}/{post.id}')
        except Exception as e:
            assert False, \
            f'''Страница подписки /username/follow/ работает неправильно, проверьте её корректность, ошибка {e}'''
        if response.status_code in (301, 302):
            response = client.get(f'/{create_post_author.username}/{post.id}/')
        assert response.status_code != 404, \
            f'''Страница /username/follow/ не найдена, проверьте корректность файла url'''

        # 2
        url = f'/{create_post_author.username}/{post.id}'
        response = client.post(url, data={
                        'text': 'Пробный комментарий!',
                    }
        )

        assert response.status_code in (301, 302), \
            f'''Некорректно перенаправляется пользователь'''
