from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q

from .models import Article, Category, Comment
from .forms import CommentForm, ArticleForm, SearchForm

#Статьи
class ArticleListView(ListView):
	model = Article
	template_name = 'article_list.html'
	context_object_name = 'articles'
	paginate_by = 2

class ArticleDetailView(DetailView):
	model = Article
	template_name = 'article_detail.html'

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
	form_class = ArticleForm
	template_name = 'article_new.html'
	login_url = 'login'
	permission_required = 'articles.add_article'
		
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


#Категории
class CategoryDetailView(DetailView):
	model = Category
	template_name = 'category_detail.html'
	context_object_name = 'category'
	pk_url_kwarg = 'cat_id'

	def get_queryset(self, *args, **wkargs):
		return Category.objects.prefetch_related('article_set')


#Комментарии
class CommentCreateView(LoginRequiredMixin, CreateView):
	form_class = CommentForm
	template_name = 'comment_new.html'
	login_url = 'login'

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.article = Article.objects.get(pk=self.kwargs.get('pk'))
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('article_detail', kwargs={'pk' : self.kwargs.get('pk')})

#Поиск
class SearchView(ListView): 
	model = Article
	context_object_name = 'article_list'
	template_name = 'search_results.html'

	def get_queryset(self):
		keyword = self.request.GET.get('keyword')
		category = self.request.GET.get('category')

		return Article.objects.filter(
			(Q(title__icontains=keyword) | Q(body__icontains=keyword)) & Q(category=category)
		)
