from django.urls import path

from . import views

urlpatterns = [
    path("group/<slug>", views.group_posts, name="group_posts"),
    path("new/", views.NewPost.as_view(), name="new_post"),
    path("", views.index, name="index"),
]