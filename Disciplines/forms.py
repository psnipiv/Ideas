from django import forms
from .models import Idea,Post

class NewIdeaForm(forms.ModelForm):
    subject = forms.CharField(label='Idea',
        widget=forms.Textarea(
            attrs={'rows': 1, 'placeholder': 'What is your new idea?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )
    message = forms.CharField(label='Description',
        widget=forms.Textarea(
            attrs={'rows': 7, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )


    class Meta:
        model = Idea
        fields = ['subject','message']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]