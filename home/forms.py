from django.forms import ModelForm, Textarea
from .models import Post,Comment


class PostCreateUpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class CommentCreate(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': Textarea(attrs={'class': 'form-control'}),
        }

