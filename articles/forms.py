from django.forms import ModelForm, CharField, Textarea
from django.core.exceptions import ValidationError

from .models import Comment, Article

class CommentForm(ModelForm):
	comment = CharField(
		max_length=250,
		label='Введите ваш комментарий',
		help_text='Комментарий максимум длинной 250 символов.',
		widget=Textarea(attrs={'placeholder':'Текст комментария'}),
		)

	class Meta:
		model = Comment
		fields = ('comment',)

	def clean_comment(self):
		value = self.cleaned_data['comment']
		if value == 'Светлый Путь':
			raise ValidationError('Запрещается упоминать название нашего инфо-посёлка!')
		return value

class ArticleForm(ModelForm):

	class Meta:
		model = Article
		fields = ('title', 'body', 'category')
		help_texts = {'title': 'Заколовок максимум 250 символов.'}