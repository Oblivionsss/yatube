from django.urls import path

from . import views

urlpatterns = [
    path("group/<slug>", views.group_posts, name="group_posts"),
    path("new/", views.new_post, name="new_post"),
    path("", views.index, name="index"),
    # профайл пользователя
    path("<str:username>", views.profile, name="profile"),
    # просмотр записи
    path("<str:username>/<int:post_id>", views.post_view, name="post"),
    path("<str:username>/<int:post_id>/edit/", 
         views.post_edit, 
         name="post_edit"),
]