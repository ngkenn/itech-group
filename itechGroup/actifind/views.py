from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from actifind.models import Review
from actifind.forms import UserForm, UserProfileForm, ActivityForm, UploadPictureForm
from actifind.models import Activity
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q
from django.db.models import Avg


def index(request):
    context_dict = {
        "activities": Activity.objects.all().annotate(avg=Avg('review__rating')).order_by('-avg')[:3]
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

@login_required
def add_activity(request):
    form = ActivityForm()
    if request.method == 'POST':
        form = ActivityForm(request.POST)
       
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
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
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # now save UserProfile model instance
                profile.save()

            # Update variable to show registration successful
            registered = True
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('index'))
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

@login_required
def add_review(request):
    activity_slug = None
    review = None

    if request.method == 'POST':
        activity_slug = request.POST['activity']
    if activity_slug:
        try:
            activity = Activity.objects.get(slug=activity_slug) 
            rating = int(request.POST['rating'])
            title = request.POST['title']
            description = request.POST['description']
            review = Review(title=title, rating=rating, message=description, activity=activity, user=request.user)
            review.save()
        except Activity.DoesNotExist:
            review = None
    
    return HttpResponse(review)

# def add_review(request, activity_name_slug):
#     try:
#         activity = Activity.objects.get(slug=activity_name_slug)
#     except Activity.DoesNotExist:
#         category = None

#     form = ReviewForm()
#     if request.method == 'POST':
#         form = PageForm(request.POST)

#         if form.is_valid():
#             if activity:
#                 review = form.save(commit=False)
#                 review.activity = activity
#                 review.save
#                 return show_activity(request, activity_name_slug)
#         else:
#             print(form.errors)

#     context_dict = {'form':form, 'activity': activity}
#     return render(request, 'actifind/add_review.html', context_dict)


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

@login_required
def upload_picture(request, activity_name_slug):
    context_dict = {}

    try: 
        activity = Activity.objects.get(slug=activity_name_slug)
        context_dict['activity'] = activity
    except Activity.DoesNotExist:
        context_dict['activity'] = None

    if activity and request.method == 'POST':
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.activity = activity
            picture.user = request.user
            picture.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UploadPictureForm()
    
    context_dict['form'] = form

    return render(request, 'actifind/upload_picture.html', context_dict) #Put where the page is


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "Please enter search keywords"
        return render(request, 'actifind/index.html', {'error_msg': error_msg})


    # | Q(description__icontains=q)
    activity_list = Activity.objects.filter(Q(name__icontains=q))
    return render(request, 'actifind/search_results.html', {'error_msg': error_msg, 'activities': activity_list})

















