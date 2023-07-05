from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Group
from .form import PostForm

def index(request):
	"""
	Отображение последних 11 постов.
	latest - временная переменная для 11 последних постов.
	"""
	post_list = Post.objects.order_by('-pub_date').all()
	paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
	
	page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
	page = paginator.get_page(page_number)  # получить записи с нужным смещением
	return render(
		request,
		'index.html',
		{'page': page, 'paginator': paginator}
   )


def group_posts(request, slug):
	"""
	Отображение последних 12 постов выбранной группы.
	group - объект с текущей группой
	slug  - текущя группа
	"""
	group = get_object_or_404(Group, slug = slug)

	# Ограничиваем выборку по группе и количеству данных 
	posts = Post.objects.filter(group = group).order_by("-pub_date")[:12]

	return render(request, "group.html", {"group": group, "posts": posts})


@login_required
def new_post(request):
	form = PostForm(request.POST or None)
	if not form.is_valid():
		return render(request, 'new_post.html', {'form': form})
	post = form.save(commit=False)
	post.author = request.user
	post.save()
	return redirect('index')