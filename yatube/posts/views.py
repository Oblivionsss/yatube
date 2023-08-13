from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .form import PostForm, CommentForm
from .models import Post, Group, User, Comment, Follow


@cache_page(15)
def index(request):
	"""
	Отображение постов.
	post_list - временная переменная для всех постов,
	paginator - постраничное разбиение постов,
	page_number - текущий номер страницы,
	page - записи по текущей странице.
	"""
	# все записи.
	post_list = Post.objects.order_by('-pub_date').all()

	# отображение по 10 записей на странице.
	paginator = Paginator(post_list, 10)  
	page_number = request.GET.get('page')
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
	slug - адрес текущей группы,
	paginator, age_number, page аналог def_index.
	"""
	# Список записей группы `group`.
	group = get_object_or_404(Group, slug = slug)

	posts = (Post.objects
		.filter(group = group)
		.order_by("-pub_date")
	)

	# отображение по 10 записей на странице.
	paginator = Paginator(posts, 10)
	page_number = request.GET.get('page')
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


# авторизованность пользователя.
@login_required
def new_post(request, ):
	"""
	Страница создания нового поста.
	form - форма на основе Post,
	post - форма с заполненными данными, готова к записи в БД.
	"""
	form = PostForm(request.POST or None)
	if not form.is_valid():
		return render(request, 'new_post.html', {'form': form})

	post = form.save(commit=False)
	post.author = request.user
	post.save()

	return redirect('index')


@login_required
def profile(request, username):
	"""
	Страница - профайл пользователя.
	author - запрашиваемый пользователь,
	list_post - список постов запрашиваемого пользователя,
	list_post_paginator, page_number, page - постраничное разбиение постов.
	"""
	# список постов запрашиваемого пользователя.
	author = get_object_or_404(User, username = username)

	list_post = (Post.objects
		.filter(author=author)
		.order_by('-pub_date').all()
	)
	
	# отображение по 5 записей на странице.
	list_post_paginator = Paginator(list_post, 5)
	page_number = request.GET.get('page')
	page = list_post_paginator.get_page(page_number)

	# информация о подписках.
	following = Follow.objects.filter(user=request.user, author=author)
	
	return render(
		request,
		'profile.html',
		{
			'page' : page,
			'author': author,
			'following': following,
			'list_post_paginator' : list_post_paginator
		}
	)


def post_view(request, username, post_id):
	"""
	Страница просмотра записи.
	post - просматриваемый пост,
	items - коемментарии к посту,
	form - форма для создания нового комменатрия,
	author - авто поста.
	"""
	# Проверка корректности адреса.
	post = get_object_or_404(Post, pk=post_id, author__username=username)
	
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
		# 1. В случае несовпадения пользователя и автора испр. поста- 
		страница просмотра поста, без возможности редактирования.
		далее - для совп. пользователя и автора испр. поста:
		# 2. Обработка внесенных изменений и возврат на страницу просмотра поста.
		# 3. Загрузка формы редактирования существующего поста.
	
	profile - испрашиваемый автор,
	post - испрашиваемый пост,
	couunt_post - количество страниц.
	"""
	profile = get_object_or_404(User, username=username)
	post = get_object_or_404(Post, pk=post_id, author=profile)

	# 1
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
	
	# 2
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect(
				'post',
				username=request.user.username,
				post_id=post_id,
			)
	
	# 3
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
def add_comment(request, username, post_id ):
	"""
	Добавление комментария.
	post - пост, к которому добавляется комментарий,
	form - форма комментария с текстом,
	comments - форма комментария - post, с автором и привязкой к посту. 
	"""
	post = get_object_or_404(Post, pk=post_id, author__username=username)

	form = CommentForm(request.POST or None)
	if not form.is_valid():
		return render(request, 'post.html', {'form': form})

	comments = form.save(commit=False)
	comments.author = request.user
	comments.post = post
	comments.save()
	
	return redirect(
			'post', 
			username=username,
			post_id=post_id,
	)


@login_required
def follow(request):
	"""
	Отображение постов из списка подписок.
	user_follows - список авторов, на которых подписан user,
	posts_follows - список постов авторов, на которых подписан user,
	paginator, page_number, page - постраничное разбиение постов.
	"""
	user_follows = (User.objects
		 .get(pk=request.user.id)
		 .follower.all().values_list('author'))

	posts_follows = (Post.objects
		  .filter(author__in=user_follows)
		  .order_by('-pub_date'))
	
	paginator = Paginator(posts_follows, 10)  
	page_number = request.GET.get('page')
	page = paginator.get_page(page_number)
	
	return render(
		request,
		'follow.html',
		{
			'page': page, 
			'paginator': paginator,
		}
	)


@login_required
def profile_follow(request, username):
	"""
	Подписка на автора.
	following - автор, на которого подписываемся,
	follow_exist - объект связка подписчика и автора.
	"""
	following = get_object_or_404(User, username=username)
	follow_exist = Follow.objects.filter(author=following,user=request.user)
	if not follow_exist and request.user.username != username:
		Follow.objects.create(author=following,user=request.user)
	return redirect(
			'profile', 
			username=username
	)


@login_required
def profile_unfollow(request, username):
	"""	
	Отписка от автора.
	following - автор, на которого подписываемся,
	follow_exist - объект связка подписчика и автора.
	"""
	unfollowing = get_object_or_404(User, username=username)
	unfollow_exist = Follow.objects.filter(author=unfollowing,user=request.user)
	if unfollow_exist and request.user.username != username:
		Follow.objects.get(author=unfollowing,user=request.user).delete()
	return redirect(
			'profile', 
			username=username
	)