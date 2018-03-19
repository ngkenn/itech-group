from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from actifind.models import Review
from actifind.forms import ReviewForm, UserForm, UserProfileForm, ActivityForm, UploadPictureForm
from actifind.models import Activity
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q


def index(request):
    context_dict = {
        "activities": Activity.objects.all().order_by('-id')[:5]
    }
    response = render(request, 'actifind/index.html', context_dict)
    return response


def show_activity(request, activity_name_slug):
    context_dict = {
        "GOOGLE_MAPS_KEY": settings.GOOGLE_MAPS_KEY
    }

    try:
        activity = Activity.objects.get(slug=activity_name_slug)
        context_dict['activity'] = activity

    except Activity.DoesNotExist:
        context_dict['activity'] = None

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


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Actifind account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'actifind/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    return render(request, 'actifind/profile.html/', {})

def upload_picture(request):    #only if logged in - set as variable in the HTML? IF Logged in etc...
    if request.method == 'POST':
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request,'actifind/upload_picture.html') #Back to index page? or to confirmation page
    else:
        form = UploadPictureForm()
    return render(request, 'actifind/upload_picture.html', {'form': form}) #Put where the page is


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "Please enter search keywords"
        return render(request, 'actifind/index.html', {'error_msg': error_msg})

    activity_list = Activity.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'actifind/index.html', {'error_msg': error_msg,
                                               'activity': activity_list})

















