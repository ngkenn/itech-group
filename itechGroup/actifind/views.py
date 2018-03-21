from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from actifind.models import Review, UserProfile, Tag, Activity
from actifind.forms import UserForm, UserProfileForm, ActivityForm, UploadPictureForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    context_dict = {
        "activities": Activity.objects.all().annotate(avg=Avg('review__rating')).order_by('-avg')[:3]
    }
    response = render(request, 'actifind/index.html', context_dict)
    return response

def about(request):
    response = render(request, 'actifind/about.html')
    return response

def all_activities(request):
    response = render(request, 'actifind/all_activities.html')
    return response

def show_activity(request, activity_name_slug):
    context_dict = {
        "GOOGLE_MAPS_KEY": settings.GOOGLE_MAPS_KEY
    }

    try:
        activity = Activity.objects.get(slug=activity_name_slug)
        context_dict['activity'] = activity

        if activity.review_set.count() > 0:
            review_list = activity.review_set.all().order_by('-id')
            paginator = Paginator(review_list, 4)
            page = int(request.GET.get('page') or 1)
            reviews = paginator.page(page)
            context_dict['reviews'] = reviews

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
            activity.lat = float(request.POST['act-lat'])
            activity.lng = float(request.POST['act-lng'])
            activity.save()

            if request.POST['tags-string']:
                tags = request.POST['tags-string'].split(",")

                for tag_name in tags:
                    tag = Tag.objects.get_or_create(name=tag_name)[0]
                    activity.tags.add(tag)

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

def show_pictures(request, activity_name_slug):
    context_dict = {}

    try:
        activity = Activity.objects.get(slug=activity_name_slug)
        context_dict['activity'] = activity
    except Activity.DoesNotExist:
        context_dict['activity'] = None

    if context_dict['activity'] and request.method == 'GET':
        pictures = activity.picture_set.all()
        if pictures.all().count() > 0:
            first_picture = pictures[0]
            context_dict["first_picture"] = first_picture
            context_dict["pictures"] = pictures[1:]

    return render(request, 'actifind/show_pictures.html', context_dict)


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
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'picture': userprofile.picture, })

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)

    return render(request, 'actifind/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})


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
    activity_list = Activity.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(address__icontains=q) | Q(activity_type__icontains=q))
    return render(request, 'actifind/search_results.html', {'error_msg': error_msg, 'activities': activity_list})


@login_required
def show_my_reviews(request):
    context_dict = {}

    if request.user and request.user.review_set.count() > 0:
        review_list = request.user.review_set.all().order_by('-id')
        paginator = Paginator(review_list, 10)
        page = int(request.GET.get('page') or 1)
        reviews = paginator.page(page)
        context_dict['reviews'] = reviews

    return render(request, 'actifind/show_my_reviews.html', context_dict)
