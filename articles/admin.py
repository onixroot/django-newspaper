from django.contrib import admin

from .models import Article, Comment, Category

# Register your models here.

class CommentInline(admin.TabularInline):
	model = Comment

class ArticleAdmin(admin.ModelAdmin):
	inlines = [CommentInline,]
	list_display = ("__str__", "get_body_short", "author", "category",)
	
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Category)
