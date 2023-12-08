from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import localtime, now

from .models import Comment, Post, User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = localtime(
            now()
        ).strftime('%Y-%m-%dT%H:%M')

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'format': '%Y-%m-%dT%H:%M',
                    }
                )
            }


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ('password',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'rows': 3,
                    }
                )
            }
