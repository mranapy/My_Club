from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Blog(models.Model):
	title = models.CharField('Blog Title',max_length=150, blank=False, null=False)
	slug = models.SlugField(max_length=264, unique=True)
	description = models.TextField('Description', max_length=400,blank=False,null=False)
	images = models.ImageField(upload_to='blog/postImages/',verbose_name='Upload Image')
	publish_date = models.DateTimeField(verbose_name='Blog date', auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)
	blog_author = models.ForeignKey(User, blank=True,on_delete=models.CASCADE)
    
