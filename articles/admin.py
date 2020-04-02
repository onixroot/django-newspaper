from django.contrib import admin
from django.utils import timezone
from django.db.models import F

from datetime import datetime, date, timedelta

from .models import Article, Comment, Category

# Register your models here.

#Статьи
class DateFilter(admin.SimpleListFilter):
	title = 'Дата публикации'
	parameter_name = 'published'

	def lookups(self, request, model_admin):
		return (
			('today', 'За сегодня'),
			('week', 'За 7 дней'),
			('month','За 30 дней'),
		)

	def queryset(self, request, queryset):
		if self.value() == 'today':
			return queryset.filter(date__date=date.today())
		elif self.value() == 'week':
			date_week_ago = timezone.now().date() - timedelta(days=7)
			return queryset.filter(date__date__gte=date_week_ago)
		elif self.value() == 'month':
			date_month_ago = timezone.now().date() - timedelta(days=30)
			return queryset.filter(date__date__gte=date_month_ago)

class CommentInline(admin.TabularInline):
	model = Comment

class ArticleAdmin(admin.ModelAdmin):
	inlines = [CommentInline,]
	list_display = ("__str__", "get_body_short", "author", "category", "date",)
	list_filter = (DateFilter,)
	search_fields = ('title', 'body',)
	# actions_on_bottom = True
	list_per_page = 5

#Комментарии
def user_ban(modeladmin, request, queryset):
	f = F('comment')
	for record in queryset:
		record.comment = 'Комментарий удалён, пользователь отключён'
		record.save()
		record.author.is_active = False
		record.author.save()
	modeladmin.message_user(request, 'Комментарий удалён, пользователь отключён')
user_ban.short_description = 'Бан за комментарий'

class CommentAdmin(admin.ModelAdmin):
	list_display = ('comment', 'article', 'author')
	fields = ('comment',)
	list_per_page = 5
	actions = (user_ban, )
	search_fields = ('comment',)


#Категории
class ArticleInline(admin.TabularInline):
	model = Article

class CategoryAdmin(admin.ModelAdmin):
	inlines = [ArticleInline,]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
