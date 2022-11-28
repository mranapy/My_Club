from django.urls import path
from Blog import views

app_name = "Blog"


urlpatterns = [
    path('create-blog/',views.createBlog, name='create-blog'),
    
]