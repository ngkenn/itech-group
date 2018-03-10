from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Review
from rango.forms import ReviewForm


def index(request):
    response = render(request, 'actifind/index.html')
    return response

def add_page(request, activity_name_slug):
    try:
        activity = Activity.objects.get(slug=activity_name_slug)
    except Activity.DoesNotExist:
        category = None

    form = ReviewForm()
    if requect.method == 'POST':
        form = PageForm(request.POST)

        if form,is_valid():
            if activity:
                review = form.save(commit=False)
                review.activity = activity
                review.save
                return shoq_activity(request, activity_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'activity': activity}
    return render(request, 'actifind/add_review.html', context_dict)
