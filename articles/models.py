from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

class Article(models.Model):
	title = models.CharField(max_length=250, verbose_name='Заголовок')
	body = models.TextField(verbose_name='Текст статьи')
	date = models.DateTimeField(auto_now_add=True)
	category = models.ForeignKey('Category', null=True, on_delete=models.PROTECT, verbose_name='Категория')
	author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Автор')

	class Meta:
		ordering = ['-date']
		verbose_name = 'Статья'
		verbose_name_plural = 'Статьи'

	def __str__(self):
		return self.title if len(self.title)<30 else self.title[:30]+'...'
		
	def get_absolute_url(self):
		return reverse('article_detail', args=[str(self.id)])

	def get_body_short(self):
		return self.body if len(self.body)<100 else self.body[:100]+'...'
	get_body_short.short_description="Текст статьи"

class Category(models.Model):
	name = models.CharField(max_length=30, db_index=True, verbose_name='Название')

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def __str__(self):
		return self.name


class Comment(models.Model):
	article = models.ForeignKey(
		Article,
		on_delete=models.CASCADE,
		related_name='comments',)
	comment = models.TextField(max_length=250)
	author = models.ForeignKey(
		get_user_model(),
		on_delete=models.CASCADE,)

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'
	
	def __str__(self):
		return self.comment
	
	def get_absolute_url(self):
		return reverse('article_list')

