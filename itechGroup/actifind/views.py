from django.shortcuts import render
from django.http import HttpResponse
from actifind.models import Review
from actifind.forms import ReviewForm, UserForm, UserProfileForm
from actifind.models import Activity


def index(request):
    response = render(request, 'actifind/index.html')
    return response


def register(request):

    registered = False

    # If its a HTTP POST, we process form data
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the forms are valid:
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = request.user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # now save UserProfile model instance
                profile.save()

            # Update variable to show registration successful
                registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
            # Invalid. Print problems to terminal
        user_form = UserForm()
        profile_form = UserProfileForm()

        #Render template
    return render(request,'actifind/register.html',
                {'user_form': user_form,
                 'profile_form': profile_form,
                    'registered': registered})


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
