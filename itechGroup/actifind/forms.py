from django import forms
from actifind.models import Activity

class ActivityForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the activity name.")
    type = forms.CharField(max_length=128,
                            help_text="Please enter activity type.")
    description = forms.Textarea()
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Activity
        fields = ('name','type','description')