from django.shortcuts import render
from django.http import HttpResponse
from actifind.models import Review
from actifind.forms import ReviewForm
from actifind.models import Activity


def index(request):
    response = render(request, 'actifind/index.html')
    return response


def register(request):
    response = render(request, 'actifind/register.html')
    return response


def add_review(request, activity_name_slug):
    try:
        activity = Activity.objects.get(slug=activity_name_slug)
    except Activity.DoesNotExist:
        category = None

    form = ReviewForm()
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if activity:
                review = form.save(commit=False)
                review.activity = activity
                review.save
                return show_activity(request, activity_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'activity': activity}
    return render(request, 'actifind/add_review.html', context_dict)
