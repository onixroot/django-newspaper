from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Article, Category, Comment

#Статьи
class ArticleListView(ListView):
	model = Article
	template_name = 'article_list.html'
	login_url = 'login'
	context_object_name = 'articles'
	paginate_by = 2

	def get_queryset(self, *args, **kwargs):
		self.category_id = self.kwargs.get('cat_id')
		if self.category_id:
			return Article.objects.filter(category=self.category_id)
		return super().get_queryset()        

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.category_id:
			context['category'] = Category.objects.get(pk=self.category_id)
		return context

class ArticleDetailView(DetailView):
	model = Article
	template_name = 'article_detail.html'
	login_url = 'login'

class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
	model = Article
	template_name = 'article_edit.html'
	fields = ('title', 'body',)
	login_url = 'login'
	permission_required = 'articles.change_article'

	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.author != self.request.user:
			raise PermissionDenied
		return super().dispatch(request, *args, **kwargs)

class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
	model = Article
	template_name = 'article_delete.html'
	success_url = reverse_lazy('article_list')
	login_url = 'login'
	permission_required = 'articles.delete_article'

	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.author != self.request.user:
			raise PermissionDenied
		return super().dispatch(request, *args, **kwargs)

class ArticleCreateView(PermissionRequiredMixin, CreateView):
	model = Article
	template_name = 'article_new.html'
	fields = ('title', 'body', 'category')
	login_url = 'login'
	permission_required = 'articles.add_article'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

#Категории
class CategoryListView(ListView):
	model = Category
	template_name = 'category_list.html'
	context_object_name = 'categories'

#Комментарии
class CommentCreateView(LoginRequiredMixin, CreateView):
	model = Comment
	template_name = 'comment_new.html'
	fields = ['comment']
	login_url = 'login'

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.article = Article.objects.get(pk=self.kwargs.get('pk'))
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('article_detail', kwargs={'pk' : self.kwargs.get('pk')})