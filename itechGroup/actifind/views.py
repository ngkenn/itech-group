from django.shortcuts import render
from django.http import HttpResponse
from actifind.models import Activity
from actifind.forms import ActivityForm
from django.conf import settings

def index(request):
    response = render(request, 'actifind/index.html')
    return response

def show_activity(request, activity_name_slug):
    context_dict = {
        "GOOGLE_MAPS_KEY": settings.GOOGLE_MAPS_KEY
    }

    try:
        activity = Activity.objects.get(slug=activity_name_slug)
        context_dict['activity'] = activity

    except Activity.DoesNotExist:
        context_dict['category'] = None

    return render(request, 'actifind/activity.html', context_dict)


def add_activity(request):
    form = ActivityForm()
    if request.method == 'POST':
        form = ActivityForm(request.POST)
       
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    
    context_dict = {
        "GOOGLE_MAPS_KEY": settings.GOOGLE_MAPS_KEY,
        "form": form
    }

    return render(request, 'actifind/add_activity.html', context_dict)