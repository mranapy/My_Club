from django.urls import path
from . import views
from Blog.views import CreateBlog,ListBlog,BlogDetailsView

app_name = "Blog"


urlpatterns = [
    path('create-blog/',CreateBlog.as_view(), name='create-blog'),
    path('list-blog/',ListBlog.as_view(), name='list-blog'),
    path('details/?P<slug>[-a-zA-Z0-9_]+)$', BlogDetailsView.as_view(), name='blog-details'),
]