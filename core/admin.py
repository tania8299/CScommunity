

from django.contrib import admin
from .models import Post, Profile,LikePost,Commnent

from django.contrib.auth.admin import UserAdmin

class ProfileAdmin(admin.ModelAdmin):
       list_display=('user','name','isverified')

# Register your models here.
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Commnent)

