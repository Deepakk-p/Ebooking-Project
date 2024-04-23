from django import forms
from account.models import Review


class ReviewForm(forms.ModelForm):
    review=forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Write review here"}))
    # rating = forms.IntegerField(label="Rating", min_value=1, max_value=5, required=False)  # Added rating field

    class Meta:
        model= Review
        fields=['review','rating']