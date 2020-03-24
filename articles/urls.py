from django.urls import path

from .views import (
	ArticleListView,
	ArticleDetailView,
	ArticleUpdateView,
	ArticleDeleteView,
	ArticleCreateView,
	CategoryListView,
	CategoryDetailView,
	)

urlpatterns = [
	path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
	path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
	path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
	path('new/', ArticleCreateView.as_view(), name='article_new'),
	path('', ArticleListView.as_view(), name='article_list'),
	path('category/<int:cat_id>/', ArticleListView.as_view(), name='category_detail'),
	path('category/', CategoryListView.as_view(), name='category_list'),
]