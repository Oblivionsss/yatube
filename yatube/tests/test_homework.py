import pytest
import re

from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model
from django.db.models import fields
from django.template.loader import get_template

try:
	from posts.models import Post
except ImportError:
	assert False, f'Не найдена модель Post'

try:
	from posts.models import Group
except ImportError:
	assert False, f'Не найдена модель Group'

def search_field(fields, attname):
	for field in fields:
		if attname == field.attname:
			return field
	return None  


class TestPost:

	# Проверка корректности модели
	def test_post_model(self):
		# проверка text в модели Post
		model_fields = Post._meta.fields
		text_field = search_field(model_fields, 'text')
		assert text_field is not None, \
			f'''Не найден атрибут `text`, проверьте корректность модели Post'''
		assert type(text_field) == fields.TextField, \
			f'''Свойство `text` модели Post должно быть текстовым TextField'''

		# проверка pub_date в модели Post
		pub_date_field = search_field(model_fields, 'pub_date')
		assert pub_date_field is not None, \
			f'''Не найден атрибут `pub_date`, проверьте корректность модели Post'''
		assert type(pub_date_field) == fields.DateTimeField, \
			f'''Свойство `pub_date` модели Post должно быть временем DateTimeField'''
		assert pub_date_field.auto_now_add, \
			f'''Свойство `pub_date` модели Post должно быть auto_now_add'''

		# проверка author в модели Post (author_id т.к. внешний ключ)
		author_field = search_field(model_fields, 'author_id')
		assert author_field is not None, \
			f'''Не найден атрибут `author`, проверьте корректность модели Post'''
		assert type(author_field) == fields.related.ForeignKey, \
			f'''Свойство `author` модели Post должно быть вненшним ключом ForeignKey'''
		assert author_field.related_model == get_user_model(), \
			f'''Свойство `author` модели Post должно быть ссылкой на модель пользователя `User`'''

		# проверка group в модели Post (group_id т.к. ссылается на модель Group)
		group_field = search_field(model_fields, 'group_id')
		assert group_field is not None, \
			f'''Не найден атрибут `group`, проверьте корректность модели Post'''
		assert type(group_field) == fields.related.ForeignKey, \
			f'''Свойство `group` модели Post должно быть вненшним ключом ForeignKey'''
		assert group_field.related_model == Group, \
			f'''Свойство `group` модели Post должно быть ссылкой на модель `Group`'''
		assert group_field.blank, \
			f'''Свойство `group` модели Post должно быть blank=True'''
		assert group_field.null, \
			f'''Свойство `group` модели Post должно быть null=True'''

	# Проверка модели с помощью создания поста
	@pytest.mark.django_db(transaction=True)
	def test_post_create(self, user):
		text = 'Тестовый пост'
		author = user

		assert Post.objects.all().count() == 0

		post = Post.objects.create(text=text, author=author) 
		assert Post.objects.all().count() == 1
		