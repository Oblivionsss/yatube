from re import L
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
	""" Структура Группы (единая тематика для постов)
	Свойства класса Группа:
	title - заголовок, наименование группы
	description - описание группы
	slug - адресное (url) наименование
	"""
	title = models.CharField(max_length=200)
	description = models.TextField()
	slug = models.SlugField(max_length=25, unique=True)

	def __str__(self):
		return self.title


class Post(models.Model):
	""" Структура Поста (публикация)
	Свойства класса Пост:
	text - содержание поста
	pub_date - дата публикации
	author - автор публикации
	group - принадлежность к группе
	"""
	text = models.TextField()
	pub_date = models.DateTimeField("date published",
									auto_now_add =True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, 
									related_name = "posts")
	group = models.ForeignKey(Group, blank=True, null=True, 
		                  			on_delete=models.CASCADE)
	image = models.ImageField(upload_to='posts/', blank=True,
			   						null=True)
	
	def __str__(self):
		return self.text