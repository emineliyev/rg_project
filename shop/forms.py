from django import forms

from shop.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['first_name', 'last_name', 'text', 'rating']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ad'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Soyad'}),
            'text': forms.Textarea(attrs={'placeholder': 'Rəy'}),
            'rating': forms.HiddenInput(),  # Скрытое поле для рейтинга
        }

