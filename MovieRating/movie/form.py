from django import forms
from .models import Review,Movie


class MovieForm(forms.Form):
    movie_name = forms.CharField(label="Movie name", max_length=100)

class MovieTypeForm(forms.Form):
    class Meta:
        model = Movie
    CATEGORY_CHOICES = (
        ('select', 'Select'),
        ('action', 'Action'),
        ('love', 'Love'),
        ('sci-fi', 'Science Fiction'),
        # Add more categories as needed
    )
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'watchAgain']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }