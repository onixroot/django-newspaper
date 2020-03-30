from django import template

register = template.Library()

@register.inclusion_tag('tags/categories_list.html')
def categories_list(categories):
	return {'categories': categories}