from django import forms
from .models import Post, PostImage


class PostForm(forms.ModelForm):
    images = forms.ImageField(
    widget=forms.FileInput(attrs={
        'accept': 'image/*',
        'class': 'form-control',
    }),
    required=False,
)

    class Meta:
        model = Post
        fields = ('title', 'community', 'twitter_link', 'comment_text', 'hashtags')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title',
            }),
            'community': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter community name',
            }),
            'twitter_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://twitter.com/...',
            }),
            'comment_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter comment text',
            }),
            'hashtags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter hashtags (comma-separated)',
            }),
        }


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image_url',)
