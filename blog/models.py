#blog/models.py
#define the data objects for our application
from django.db import models

# Create your models here.
#needed to inherit fromthe model


class Article(models.Model):
    '''encapsulate the idea of on eArticle by some author'''
    #data attributes of an article
    title = models.TextField(blank = False)
    author = models.TextField(blank = False)
    text = models.TextField(blank = False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this object'''
        return f'{self.title} by {self.author}'
    
class Comment(models.Model):
        '''model the one to many relationship with Article'''
        article = models.ForeignKey("Article", on_delete=models.CASCADE)
        author = models.TextField(blank = False)
        text = models.TextField(blank = False)
        published = models.DateTimeField(auto_now=True)

        def __str__(self):
            '''return strig repesentation of coment'''
            return f'{self.text}'