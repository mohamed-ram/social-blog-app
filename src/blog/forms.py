from django import forms
from .models import Comment, Post
from django.utils import timezone


class CustomDateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'text', 'image', 'publish_at', 'category', 'tags', 'publish'
        ]
        widgets = {
            'publish_at': CustomDateTimeInput(attrs={'class': 'timepicker'}),
        }


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'text', 'image', 'category', 'tags', 'publish'
        ]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField(max_length=50)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']





