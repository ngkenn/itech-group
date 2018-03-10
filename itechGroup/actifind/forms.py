from django import forms
from rango.models import Review, Activity, Picture

class ReviewForm(forms.modelForm):
    title = forms.CharField(max_length=128)
    date = forms.DateField(widget=forms.HiddenInput())
    rating = forms.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    article = models.ForeignKey(Activity)
    class Meta:
        model = Review
        
