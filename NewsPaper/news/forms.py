from django import forms
from news.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'autor',
            'post_type',
            'post_categories',
            'post_title',
            'post_text',
        ]
