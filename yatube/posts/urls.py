from django.urls import path

from . import views

urlpatterns = [
     # просмотр группы
     path("group/<slug>", views.group_posts, name="group_posts"),

     # создание нового поста 
     path("new", views.new_post, name="new_post"),

     path("follow", views.follow, name="follow_index"),
     # Главная страница
     path("", views.index, name="index"),

     # профайл пользователя
     path("<str:username>", views.profile, name="profile"),

     # просмотр записи
     path("<str:username>/<int:post_id>", views.post_view, name="post"),
     path("<str:username>/<int:post_id>/edit/", 
         views.post_edit, 
         name="post_edit"),
     path('str:<username>/<int:post_id>/comment',
         views.add_comment, name='add_comment'),

     # подписка
     path("<str:username>/follow/", views.profile_follow, name="profile_follow"),
     path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
]