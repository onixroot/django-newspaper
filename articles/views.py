from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Article, Category

# Create your views here.

class ArticleListView(ListView):
	model = Article
	template_name = 'article_list.html'
	login_url = 'login'
	context_object_name = 'articles'
	paginate_by = 2

	def get_queryset(self):
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

	def get_object(self):
		return get_object_or_404(Article, pk=self.kwargs.get('pk'))

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
	fields = ('title', 'body',)
	login_url = 'login'
	permission_required = 'articles.add_article'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class CategoryListView(ListView):
	model = Category
	template_name = 'category_list.html'
	context_object_name = 'categories'

class CategoryDetailView(DetailView):
	model = Category
	template_name = 'category_detail.html'

	def get_object(self):
		return get_object_or_404(Category, pk=self.kwargs.get('cat_id'))