from re import L
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
	""" Структура Группы (единая тематика для постов).
	Свойства класса Группа:
	title - заголовок, наименование группы,
	description - описание группы,
	slug - адресное (url) наименование.
	"""
	title = models.CharField(max_length=200)
	description = models.TextField()
	slug = models.SlugField(max_length=25, unique=True)

	def __str__(self):
		return self.title


class Post(models.Model):
	""" Структура Поста (публикация).
	Свойства класса Пост:
	text - содержание поста,
	pub_date - дата публикации,
	author - автор публикации,
	group - принадлежность к группе.
	"""
	text = models.TextField()
	pub_date = models.DateTimeField('date published',
									auto_now_add =True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, 
									related_name = 'posts')
	group = models.ForeignKey(Group, blank=True, null=True, 
		                  			on_delete=models.CASCADE)
	image = models.ImageField(upload_to='tests/', blank=True,
			   						null=True)
	
	def __str__(self):
		return self.text


class Comment(models.Model):
	"""Структура Комментария.
	Свойства класс:
	text - содержание комментария,
	created - дата публикации,
	author - автор публикации.
	"""
	text = models.TextField()
	post = models.ForeignKey(Post, on_delete=models.CASCADE,
			  						related_name='comments')
	author = models.ForeignKey(User, on_delete=models.CASCADE, 
									related_name = 'comments')
	created = models.DateTimeField('date published',
									auto_now_add =True)


class Follow(models.Model):
	"""Подписка.
	user - пользователь, который подписывается,
	author - пользователь на которого подписались.
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE,
									related_name='follower',
									blank=False, null=False)
	author = models.ForeignKey(User, on_delete=models.CASCADE,
									related_name='following',
									blank=False, null=False)