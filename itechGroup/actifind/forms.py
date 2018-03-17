from django import forms
from actifind.models import Activity

class ActivityForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the activity name.")
    type = forms.CharField(max_length=128,
                            help_text="Please enter activity type.")
    description = forms.CharField(widget=forms.Textarea, help_text="Please write description.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    address = forms.CharField(max_length=516, help_text= "Please enter address")

    class Meta:
        model = Activity
        fields = ('name','type','description', 'address')