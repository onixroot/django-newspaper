from django.urls import path
from django.views.decorators.http import condition

from .views import (
	ArticleListView,
	ArticleDetailView,
	ArticleUpdateView,
	ArticleDeleteView,
	ArticleCreateView,
	CommentCreateView,
	CategoryDetailView,
	SearchView,
	article_lmf,
	)

urlpatterns = [
	path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
	path('<int:pk>/', condition(last_modified_func=article_lmf)(ArticleDetailView.as_view()), name='article_detail'),
	path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
	path('<int:pk>/comment_new', CommentCreateView.as_view(), name='comment_new'),
	path('article_new/', ArticleCreateView.as_view(), name='article_new'),
	path('', ArticleListView.as_view(), name='article_list'),
	path('category/<int:cat_id>/', CategoryDetailView.as_view(), name='category_detail'),
	path('search/', SearchView.as_view(), name='search'),
]