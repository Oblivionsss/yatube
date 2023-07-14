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

def search_refind(execution, user_code):
	"""Поиск запуска"""
	for temp_line in user_code.split('\n'):
		if re.search(execution, temp_line):
			return True
	return False


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
		assert Post.objects.get(text=text, author=author).pk == post.pk
	
	# Проверка модели Post в админке 
	def test_post_admin(self):

		admin_site = site

		assert Post in admin_site._registry, \
			f'''Зарегистрируйте модель Post в модели admin'''
		
		admin_model = admin_site._registry[Post]

		assert 'text' in admin_model.list_display, \
			f'''Добавьте `text` в для отображения в списке адм. сайта'''
		assert 'pub_date' in admin_model.list_display, \
			f'''Добавьте `pub_date` в для отображения в списке адм. сайта'''
		assert 'author' in admin_model.list_display, \
			f'''Добавьте `author` в для отображения в списке адм. сайта'''
		
		assert 'text' in admin_model.search_fields, \
			f'''Добавьте `text` для поиска в адм. сайте'''
		
		assert 'pub_date' in admin_model.list_filter, \
			f'''Добавьте `pub_date` для фильтрации в адм. сайте'''
		
		assert hasattr(admin_model, 'empty_value_display'), \
			f'''Добавьте `empty_value_display` для пустых полей'''
		

class TestGroup:
	
	# Проверка корректности модели
	def test_group_model(self):
		model_fields = Group._meta.fields
		title_field = search_field(model_fields, 'title')
		assert title_field is not None, \
			f'''Не найден атрибут `title`, проверьте корректность модели Group'''
		assert type(title_field) == fields.CharField, \
			f'''Свойство `title` модели Group должно быть текстовым CharField'''
		assert title_field.max_length == 200, \
			f'''Свойство `title` модели Group должно иметь max_length=250'''

		description_field = search_field(model_fields, 'description')
		assert description_field is not None, \
			f'''Не найден атрибут `description`, проверьте корректность модели Group'''
		assert type(description_field) == fields.TextField, \
			f'''Свойство `description` модели Post должно быть текстовым TextField'''
		
		slug_field = search_field(model_fields, 'slug')
		assert slug_field is not None, \
			f'''Не найден атрибут `slug`, проверьте корректность модели Group'''
		assert type(slug_field) == fields.SlugField, \
			f'''Свойство `slug` модели Post должно быть текстовым SlugField'''
		assert slug_field.max_length == 25, \
			f'''Свойство `slug` модели Group должно иметь max_length=25'''
		assert slug_field.unique, \
			f'''Свойство `slug` модели Group должно иметь unique=True (уникальным)'''
		
	# Проверка модели с помощью создания группы
	@pytest.mark.django_db(transaction=True)
	def test_group_create(self, user):
		text = 'Тестовый пост'
		author = user

		assert Post.objects.all().count() == 0

		post = Post.objects.create(text=text, author=author) 
		assert Post.objects.all().count() == 1
		assert Post.objects.get(text=text, author=author).pk == post.pk

		title = 'Тестовая группа'
		slug = 'test-link'
		description = 'Тестовое описание группы'
		group = Group.objects.create(title=title, slug=slug, description=description)
		assert Group.objects.all().count() == 1
		assert Group.objects.get(slug=slug).pk == group.pk

		post.group = group
		post.save()
		assert Post.objects.get(text=text, author=author).group == group


class TestGroupView:

	@pytest.mark.django_db(transaction=True)
	def test_group_view(self, client, post_with_group):
		try:
			response = client.get(f'/group/{post_with_group.group.slug}')
		except Exception:
			assert False, f'''неправильно работает страница /group/slug, ошибка {e}'''
		if response.status_code in (301, 302):
			response = client.get(f'/group/{post_with_group.group.slug}')
		assert response.status_code != 404, \
			f'''Страница `/group/<slug>/` не найдена, проверьте этот адрес в *urls.py*'''
		group = post_with_group.group
		html = response.content.decode()

		html_template = get_template('group.html').template.source
		
		assert search_refind(r'{%\s*for\s+.+in.*%}', html_template), \
			'Отредактируйте HTML-шаблон, используйте тег цикла'
		assert search_refind(r'{%\s*endfor\s*%}', html_template), \
			'Отредактируйте HTML-шаблон, не найден тег закрытия цикла'
		assert re.search(
			r'<\s*title\s*>\s*Записи\s+сообщества\s+' + group.title + r'\s+\|\s+Yatube\s*<\s*\/title\s*>',
			html
		), 'Отредактируйте HTML-шаблон, не найдено название страницы `<title>Записи сообщества {{ название_группы }} | Yatube</title>`'
		assert re.search(
			r'<\s*h1\s*>\s*' + group.title + r'\s*<\s*\/h1\s*>',
			html
		), 'Отредактируйте HTML-шаблон, не найден заголовок группы `<h1>{{ название_группы }}</h1>`'
		assert re.search(
			r'<\s*p\s*>\s*' + group.description + r'\s*<\s*\/p\s*>',
			html
		), 'Отредактируйте HTML-шаблон, не найдено описание группы `<p>{{ описание_группы }}</p>`'
		
		assert re.search(
			r'<\s*p(\s+class=".+"|\s*)>\s*' + post_with_group.text + r'\s*<\s*\/p\s*>',
			html
		), f'''Отредактируйте HTML-шаблон, не найден текст поста `<p>{{ текст_поста }}</p>`'''