from django.contrib import admin
from Blog.models import Blog

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin): # For backend 
	fields = ('title','slug','description','images','blog_author')
	list_display = ('title','publish_date','blog_author')
	list_filter = ('publish_date','title')
	search_fields = ('title',)