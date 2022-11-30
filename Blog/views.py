from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from django import template
register = template.Library()
from django.urls import  reverse
import uuid
from Blog.models import Blog
from django.views.generic import CreateView,ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from Blog.forms import CreateBlogForm
# Create your views here.
# def createBlog(request):
#     return HttpResponse('OK')
from django.views.generic.edit import FormView
slug_url_kwarg = 'slug'
class CreateBlog(LoginRequiredMixin, FormView):
    form_class = CreateBlogForm
    template_name = 'create_blog.html'
    fields = ("title","description","images")

    def form_valid(self,form):
        blog_obj = form.save(commit=False)
        blog_obj.blog_author = self.request.user
        title = blog_obj.title
        blog_obj.slug = title.replace(" ", "_") + "_" + str(uuid.uuid4())
        # blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('Blog:list-blog'))

class ListBlog(ListView):
    model = Blog
    context_object_name = 'listblog'
    template_name='blog_list.html'

class BlogDetailsView(DetailView):
    model = Blog
    context_object_name = 'blogdetails'
    template_name='blog_details.html'
