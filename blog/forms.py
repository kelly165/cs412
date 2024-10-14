#blog/forms.py

from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    '''a form to add a comment on an article to the database'''

    class Meta:
        '''associate this form w a comment data model'''
        model = Comment
        fields = ['article', 'author', 'text']