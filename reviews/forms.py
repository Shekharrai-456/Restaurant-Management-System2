from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Stars') for i in range(1, 6)])
        }

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment.strip()) < 10:
            raise forms.ValidationError("Comment must be at least 10 characters long.")
        return comment
