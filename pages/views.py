from django.shortcuts import render
from django.views.generic import TemplateView

from articles.models import Category
from articles.forms import SearchForm

# Create your views here.

class HomePageView(TemplateView):
	template_name = 'home.html'