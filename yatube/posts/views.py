from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Group, User
from .form import PostForm


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
		{'page': page, 'paginator': paginator}
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

	return render(
		request, 
		"group.html", 
		{"group": group, "posts": posts}
	)


@login_required
def new_post(request):
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
	list_post = Post.objects.filter(author=user_profile).all()
	# показываем по пять страниц
	list_post_paginator = Paginator(list_post, 5)
	# переменная url с количеством страниц
	page_number = request.GET.get('page')
	# получить записи с нужным смещением
	page = list_post_paginator.get_page(page_number)

	count_post = len(list_post)
	
	return render(
		request,
		'profile.html',
		{
			'page' : page,
			'count_post' : count_post,
			'user_profile': user_profile,
			'list_post_paginator' : list_post_paginator,
		}
	)


def post_view(request, username, post_id):
	"""
	Страница просмотра записи.
	"""
	post = get_object_or_404(Post, pk=post_id)

	check_user = None
	if post.author == request.user:
		check_user = True
	return render(
		request,
		'post.html',
		{
			'post': post,
			'userame': request.user,
			'check_user': check_user,
		}
	)


def post_edit(request, username, post_id):
	"""
	Страница редактирования записи.
	"""
	pass
	# return render(
	# 	request,
	# 	post_new.html,
	# 	{}
	# )