import pytest

from django.contrib.auth.models import User

from posts.models import Follow, Post


class TestFollow:

	# Проверка подписки на двух авторов
	# После подписки проверяем following
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
		# проверка подписки пользователя на самого себя
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


class TestFollowView:
	@pytest.mark.django_db(transaction=True)
	def test_index_follow_get(self, client):
		# Пользователь, который подписывается
		user_follower1 = User.objects.create(username='sarah_conor',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)

		# Пользователь, который не подписывается
		user_follower2 = User.objects.create(username='john_wick',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)

		# Пользователь, на которого будем подисываться, user2
		user_following = User.objects.create(username='terminator',
			email='conor@gmail.com',
			password='12345ASDFqwer',
		)
		
		client.force_login(user_follower1)

		post_1 = Post.objects.create(text='Тестовый пост_1', author=user_following)
		post_2 = Post.objects.create(text='Тестовый пост_2', author=user_following)

		response_1 = client.get('/')
		assert response_1.status_code == 200, \
			f'''Проверьте, что Вы авторизовались `user_follower1`'''
		assert post_1.text and post_2.text in response_1.content.decode(), \
			f'''Проверьте, что вы создали правильно посты'''
		
		# попдисываемся на пользователя user_following
		try:
			response_1 = client.get(f'/{user_following.username}/follow')
		except Exception as e:
			assert False, \
			f'''Страница подписки /username/follow/ работает неправильно, проверьте её корректность, ошибка {e}'''
		if response_1.status_code in (301, 302):
			response_1 = client.get(f'/{user_following.username}/follow/')
		assert response_1.status_code != 404, \
			f'''Страница /username/follow/ не найдена, проверьте корректность файла url'''
		
		assert response_1.status_code != 400, \
			f'''Проверьте, что Вы авторизовались `user_follower1`'''
		
		assert user_follower1.follower.count() and user_following.following.count() == 1, \
			f'''Проверьте, что корректно работает подписка'''
		
		# проверка постов автора, на которого подписан user_follower1
		try:
			response_1 = client.get(f'/follow')
		except Exception as e:
			assert False, \
			f'''Страница подписки /follow/ работает неправильно, проверьте её корректность, ошибка {e}'''
		if response_1.status_code in (301, 302):
			response_1 = client.get(f'/follow/')
		assert response_1.status_code != 404, \
			f'''Страница /follow/ не найдена, проверьте корректность файла url'''

		assert response_1.status_code == 200, \
			f'''Проверьте, что Вы авторизовались `user_follower1`'''
		assert post_1.text and post_2.text in response_1.content.decode(), \
			f'''Проверьте, что вы создали правильно посты'''
		
		client.force_login(user_follower2)
		response_1 = client.get('/')
		assert response_1.status_code == 200, \
			f'''Проверьте, что Вы авторизовались `user_follower1`'''
		assert post_1.text and post_2.text in response_1.content.decode(), \
			f'''Проверьте, что вы создали правильно посты'''
		
		# проверка, что пользователь user_follower2 ни на кого не подписан
		assert user_follower2.follower.count() == 0 and user_follower2.following.count() == 0, \
			f'''Проверьте, правльно ли вы указали username'''
		
		# проверка постов автора, на которго подписан user_follower2
		try:
			response_2 = client.get(f'/follow')
		except Exception as e:
			assert False, \
			f'''Страница подписки /follow/ работает неправильно, проверьте её корректность, ошибка {e}'''
		if response_2.status_code in (301, 302):
			response_2 = client.get(f'/follow/')
		assert response_2.status_code != 404, \
			f'''Страница /follow/ не найдена, проверьте корректность файла url'''
		
		assert response_2.status_code == 200, \
			f'''Проверьте, что Вы авторизовались `user_follower1`'''
		assert post_1.text and post_2.text not in response_2.content.decode(), \
			f'''Проверьте, что вы создали правильно посты'''