from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Post, Group
from .form import CreateNewPostModelForm

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


class NewPost(CreateView):
	form_class = CreateNewPostModelForm
	success_url = reverse_lazy("index")
	template_name = "new_post.html"
	