from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Group, User, Comment
from .form import PostForm, CommentForm

from django.views.decorators.cache import cache_page


@cache_page(15)
def index(request):
	"""
	Отображение последних 11 постов.
	post_list - временная переменная для всех постов,
	paginator - постраничное разбиение постов,
	page_number - текущий номер страницы,
	page - записи по текущей странице.
	"""
	# получить все записи.
	post_list = Post.objects.order_by('-pub_date').all()
	# показывать по 10 записей на странице.
	paginator = Paginator(post_list, 10)  
	# переменная в URL с номером запрошенной страницы.
	page_number = request.GET.get('page')
	# получить записи с нужным смещением.
	page = paginator.get_page(page_number)
	
	return render(
		request,
		'index.html',
		{
			'page': page, 
			'paginator': paginator,
		}
   )


def group_posts(request, slug):
	"""
	Отображение последних 12 постов выбранной группы.
	group - объект с текущей группой,
	slug - текущя группа.
	"""
	# получение объекта группы с нужным slug'ом.
	group = get_object_or_404(Group, slug = slug)
	# Ограничиваем выборку по группе и количеству данных.
	posts = (Post.objects
	  .filter(group = group)
	  .order_by("-pub_date")[:12]
	)
	# показывать по 10 записей на странице.
	paginator = Paginator(posts, 10)
	# переменная в URL с номером запрошенной страницы.
	page_number = request.GET.get('page')
	# получить записи с нужным смещением.
	page = paginator.get_page(page_number)


	return render(
		request, 
		"group.html", 
		{
			"group": group,
			"page": page,
			"paginator": paginator,
		}
	)


@login_required
def new_post(request, ):
	"""
	Страница создания нового поста.
	form - форма на основе Post,
	post - форма с заполненными данными, готова к записи в БД.
	"""
	form = PostForm(request.POST or None)
	# проверка на наличие метода is_valid, и валидность.
	if not form.is_valid():
		return render(request, 'new_post.html', {'form': form})
	# сохраняем текущие данные.
	post = form.save(commit=False)
	post.author = request.user
	post.save()

	return redirect('index')


def profile(request, username):
	"""
	Страница - профайл пользователя.
	user_profile - запрашиваемый пользователь,
	list_post - список постов запрашиваемого пользователя,
	list_post_paginator - постраничное разбиение постов,
	page_number - юрл-номер страницы,
	page - записи по текущей странице,
	count_page - количество записей пользователя username.
	"""
	# проверка username
	user_profile = get_object_or_404(User, username = username)
	# список постов запрашиваемого пользователя
	list_post = (Post.objects
	     .filter(author=user_profile)
		 .order_by('-pub_date').all()
		)
	# показываем по пять страниц
	list_post_paginator = Paginator(list_post, 5)
	# переменная url с количеством страниц
	page_number = request.GET.get('page')
	# получить записи с нужным смещением
	page = list_post_paginator.get_page(page_number)
	#проверка авторизованности просматриваемого поста
	check_login_author = None
	if str(request.user) == str(username):
		check_login_author = True

	count_post = len(list_post)
	
	return render(
		request,
		'profile.html',
		{
			'page' : page,
			'count_post' : count_post,
			'user_profile': user_profile,
			'list_post_paginator' : list_post_paginator,
			'check_login_author': check_login_author,
		}
	)


def post_view(request, username, post_id):
	"""
	Страница просмотра записи.
	"""
	# Проверка корректности адреса
	post = get_object_or_404(Post, pk=post_id, author__username=username)
	
	# подсчет количества постов автора испрашиваемого поста
	user_profile = get_object_or_404(User, username = username)

	form = CommentForm(request.POST or None)

	items = (Comment.objects
	 	.filter(post=post)
		.order_by("-created")
	)
	return render(
		request,
		'post.html',
		{
			'post': post,
			'items': items,
			'form': form,
			'author': post.author,
		}
	)


def post_edit(request, username, post_id):
	"""
	Страница редактирования записи.
	
	Функция работает нескольких режимах:
		1. В случае несовпадения пользователя и автора испр. поста- 
		страница просмотра поста, без возможности редактирования.
		далее - для совп. пользователя и автора испр. поста:
		2. Загрузка формы редактирования существующего поста.
		3. Обработка внесенных изменений и возврат на страницу просмотра поста.
	
	profile - испрашиваемый автор,
	post - испрашиваемый пост,
	couunt_post - количество страниц.
	"""
	profile = get_object_or_404(User, username=username)
	post = get_object_or_404(Post, pk=post_id, author=profile)

	if request.user != profile:
		return redirect(
			'post', 
			username=username,
			post_id=post_id,
		)
	
	form = PostForm(
		request.POST or None,
		files=request.FILES or None,
		instance=post,
		)
	
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect(
				'post',
				username=request.user.username,
				post_id=post_id,
			)
	
	return render(
		request,
		'new_post.html',
		{
			'form': form,
			'post': post,
		}
	)


def page_not_found(request, exception):
	return render(
		request,
		"misc/404.html",
		{
			"path": request.path
		},
		status=404
	)


def server_error(request):
	return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, username, post_id, ):
	# Проверка существования поста, к которому будет добавлен кооментарий
	post = get_object_or_404(Post, pk=post_id, author__username=username)

	form = CommentForm(request.POST or None)
	# проверка на наличие метода is_valid, и валидность.
	if not form.is_valid():
		return render(request, 'post.html', {'form': form})
	# сохраняем текущие данные.
	comments = form.save(commit=False)
	comments.author = request.user
	comments.post = post
	comments.save()
	
	return redirect(
			'post', 
			username=username,
			post_id=post_id,
		)
