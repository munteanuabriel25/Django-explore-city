from django.contrib import admin
from .models import Post, Comment,Tag

# Register your models here.



class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    
class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "url"]

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag,TagAdmin)

