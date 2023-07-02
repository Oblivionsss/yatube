from django.forms import ModelForm
from .models import Post

class CreateNewPostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'author', 'group', ]
