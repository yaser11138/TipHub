from django import forms
from .models import Comment

class CommentAddForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("body",)

