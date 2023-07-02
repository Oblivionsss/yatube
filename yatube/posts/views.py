from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Post, Group
from .form import PostForm

def index(request):
	"""
	Отображение последних 11 постов.
	latest - временная переменная для 11 последних постов.
	"""
	latest = Post.objects.order_by("-pub_date")[:11]
	return render(request, "index.html", {"posts": latest})


def group_posts(request, slug):
	"""
	Отображение последних 12 постов выбранной группы.
	group - объект с текущей группой
	slug - текущя группа
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