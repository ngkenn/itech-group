from django import forms
from actifind.models import Review, Activity, Picture

class ReviewForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    date = forms.DateField(widget=forms.HiddenInput())
    rating = forms.IntegerField()
    class Meta:
        model = Review
        exclude= ('activity',)
