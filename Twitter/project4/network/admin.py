from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ["username","email","password","first_name","last_name","date_joined","image"]

class PostAdmin(admin.ModelAdmin):
    list_display = ["owner","content","time"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ["content_of_comment","post_comment","comment_owner","date_of_comment"]

class FollowersAdmin(admin.ModelAdmin):
    list_display = ["user","following"]

class LikedPostAdmin(admin.ModelAdmin):
    list_display =["post","post_owner","liker","timestamp"]


class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ["sender","receiver","content","timestamp","read"]


admin.site.register(User,UserAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Followers,FollowersAdmin)
admin.site.register(LikedPost,LikedPostAdmin)
admin.site.register(DirectMessage,DirectMessageAdmin)
