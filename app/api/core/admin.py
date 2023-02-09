from django.contrib import admin
from core.models import Page, Post, Media


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass