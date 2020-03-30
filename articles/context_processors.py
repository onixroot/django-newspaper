from articles.models import Category
from articles.forms import SearchForm

def categories_and_search(request):
    return {'categories': Category.objects.only('name'),
            'search_form': SearchForm}