#blog.views.py
#define the views for the blog app
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import * #import the models e.g. article
from .forms import *

import random

#class-based view
class ShowAllView(ListView):
    '''the view to show all Articles'''
    model = Article #the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' #context var to use in the template

class CreateCommentView(CreateView):
    '''a view to create a comment on article'''
    from_class = CreateCommentForm
    template_name = "create_comment_form.html"
    
