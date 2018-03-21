from django import forms
from actifind.models import Activity
from actifind.models import Review, Activity, Picture, UserProfile
from django.contrib.auth.models import User

#Form to add an activity
class ActivityForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the activity name.")
    activity_type = forms.CharField(max_length=128,
                            help_text="Please enter activity type.")
    description = forms.CharField(widget=forms.Textarea, help_text="Please write description.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    address = forms.CharField(max_length=516, help_text= "Please enter address")

    class Meta:
        model = Activity
        fields = ('name','activity_type','description', 'address')


#Form to add a new user
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        help_texts = {
            'username': None,
        }
        fields = ('username', 'email', 'password')

#Create a new user profile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

#Upload Picture form
class UploadPictureForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    class Meta:
        model = Picture
        fields = ('name', 'description', 'picture', )
