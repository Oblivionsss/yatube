import pytest
from django.contrib.auth.models import User
from posts.models import Follow, Post


class TestFollow:

	@pytest.mark.django_db(transaction=True)
	def test_follow_auth_user(self, client):
		# Пользователь, на которого будем подисываться, user1
		user_following = User.objects.create(username='sarah_conor',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)

		# Пользователь, на которого будем подисываться, user2
		user_following_2 = User.objects.create(username='john_wick',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)

		# Пользователь, который подписывается
		user_follower = User.objects.create(username='terminator',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)

		# авторизация
		client.force_login(user_follower)

		assert User.objects.count() == 3, \
			f'''Проверьте, что вы создали пользователей. Проверьте необходимые поля!'''

		following = [
			user_following.username,
			user_following_2.username,
		]
		
		# подписываемся на пользователей user1 и user2	
		for try_follow in following:
			try:
				response = client.get(f'/{try_follow}/follow')
			except Exception as e:
				assert False, \
				f'''Страница подписки /username/follow/ работает неправильно, проверьте её корректность, ошибка {e}'''
			if response.status_code in (301, 302):
				response = client.get(f'/{try_follow}/follow/')
			assert response.status_code != 404, \
				f'''Страница /username/follow/ не найдена, проверьте корректность файла url'''


		# количество подписок на авторов - 2
		list_follows = (User.objects
			.get(pk=user_follower.id)
			.follower.all().values_list('author'))

		assert len(list_follows) == 2, \
			f'''Проверьте корректность подписок, список подписок на авторов пуст '''


		# отпишемся от одного из авторов
		try:
			response = client.get(f'/{user_following.username}/unfollow')
		except Exception as e:
			assert False, \
			f'''Страница подписки /username/follow/ работает неправильно, проверьте её корректность, ошибка {e}'''
		if response.status_code in (301, 302):
			response = client.get(f'/{user_following.username}/unfollow/')
		assert response.status_code != 404, \
			f'''Страница /username/follow/ не найдена, проверьте корректность файла url'''

		# количество подписок на авторов - 1
		list_follows = (User.objects
			.get(pk=user_follower.id)
			.follower.all().values_list('author'))

		assert len(list_follows) == 1, \
			f'''Проверьте корректность подписок, список подписок на авторов пуст '''

	@pytest.mark.django_db(transaction=True)	
	def test_follow_myself(self, client):
		user_following = User.objects.create(username='sarah_conor',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)

		# Пользователь, который подписывается
		user_follower = User.objects.create(username='terminator',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)

		# авторизация
		client.force_login(user_follower)

		# проверка отсутствия возможности подписки на самого себя
		assert user_follower.follower.count() == 0, \
			f'''Проверьте, что правильно считается подписки'''

		try:
			response = client.get(f'/{user_follower.username}/follow')
		except Exception as e:
			assert False, \
			f'''Страница подписки /username/follow/ работает неправильно, проверьте её корректность, ошибка {e}'''
		if response.status_code in (301, 302):
			response = client.get(f'/{user_follower.username}/follow/')
		assert response.status_code != 404, \
			f'''Страница /username/follow/ не найдена, проверьте корректность файла url'''

		# количество подписок на самого себя не изменилось после поытки подписаться на себя
		assert user_follower.following.count() == 0, \
			f'''Проверьте, что правильно считается подписки'''