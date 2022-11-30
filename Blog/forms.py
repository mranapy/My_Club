from django import forms
from Blog.models import Blog
class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title','description','images')
        # fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':'5'})
        }