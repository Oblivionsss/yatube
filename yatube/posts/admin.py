from django.contrib import admin

from .models import Post, Group, Comment, Follow


class PostAdmin(admin.ModelAdmin):
	list_display = ("text", "pub_date", "author")
	search_fields = ("text",)
	list_filter = ("pub_date",)
	empty_value_display = ("-пусто-")


admin.site.register(Post, PostAdmin)


class GroupAdmin(admin.ModelAdmin):
	list_display = ("title", "description")
	empty_value_display = ("-пусто-")


admin.site.register(Group, GroupAdmin)


class CommentAdmin(admin.ModelAdmin):
	list_display = ("text", "created", "author")
	search_fields = ("text",)
	list_filter = ("created",)
	empty_value_display = ("-пусто-")


admin.site.register(Comment, CommentAdmin)


class FollowAdmin(admin.ModelAdmin):
	list_display = ("user", "author")


admin.site.register(Follow, FollowAdmin)