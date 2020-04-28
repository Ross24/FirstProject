from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	content =  models.TextField()
	date_posted = models.DateTimeField(default=timezone.now())
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	url = models.SlugField(max_length=500, blank=True)
	#url= models.SlugField(max_length=500, unique=True, blank=True)

	def save(self, *args, **kwargs):
		self.url= slugify(self.title)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title 

	def get_absolute_url(self):
		#return reverse('article_detail', kwargs={'slug': self.slug})
		return reverse('post-detail', kwargs={'pk_slug': self.slug})

	#def get_absolute_url(self):
	#	return reverse('post-detail', kwargs={'slug': self.url})
		#

	#def get_absolute_url(self):
		#return reverse('article_detail', kwargs={'pk':self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField() 
    created_on= models.DateTimeField(default = timezone.now())
    active = models.BooleanField(default=False)
    url= models.SlugField(max_length=500, blank=True)
    #url= models.SlugField(max_length=500, unique=True, blank=True)
    

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

    def save(self, *args, **kwargs):
        self.url= slugify(self.post)
        #self.url= slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
    	return reverse('article_detail', kwargs={'slug': self.slug})
    	#return self.post.get_absolute_url()
    	