from django import forms
from actifind.models import Review, Activity, Picture, UserProfile
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    date = forms.DateField(widget=forms.HiddenInput())
    rating = forms.IntegerField()
    class Meta:
        model = Review
        exclude= ('activity',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')