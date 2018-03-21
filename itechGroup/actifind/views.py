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

## VIEWS WERE LOGIN IS NOT REQUIRED ###

# Serve the index page
def index(request):
    context_dict = {
        "activities": Activity.objects.all().annotate(avg=Avg('review__rating')).order_by('-avg')[:3] # Get the 3 activities with the best rating
    }
    response = render(request, 'actifind/index.html', context_dict)
    return response

# Serve about page
def about(request):
    response = render(request, 'actifind/about.html')
    return response

# Serve activity page
def show_activity(request, activity_name_slug):
    # Get google maps key from settings
    context_dict = {
        "GOOGLE_MAPS_KEY": settings.GOOGLE_MAPS_KEY
    }

    try:
        # Try finding the activity from the slug
        activity = Activity.objects.get(slug=activity_name_slug)
        context_dict['activity'] = activity

        # If there are reviews initialize paginator with those reviews
        if activity.review_set.count() > 0:
            review_list = activity.review_set.all().order_by('-id')
            paginator = Paginator(review_list, 4)       # limit 4 per page
            page = int(request.GET.get('page') or 1)    # get requested page
            reviews = paginator.page(page) 
            context_dict['reviews'] = reviews

    # Reset if activity was not found
    except Activity.DoesNotExist:
        context_dict['activity'] = None

    return render(request, 'actifind/activity.html', context_dict)

# Serve registration page
def register(request):

    registered = False

    # If its a HTTP POST, we process form data
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the forms are valid:
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Set password hash
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # Get picture if it is attached
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Save UserProfile model instance
                profile.save()

            # Update variable to show registration successful
            registered = True

            # Login user
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Redirect to index
            return HttpResponseRedirect(reverse('index'))
        else:
            print(user_form.errors, profile_form.errors)    # Print errors
    else:
            # Invalid. Print problems to terminal
        user_form = UserForm()
        profile_form = UserProfileForm()

        #Render template
    return render(request,'actifind/register.html',
                {'user_form': user_form,
                 'profile_form': profile_form,
                    'registered': registered})


# Serve show all pictures page from activity
def show_pictures(request, activity_name_slug):
    context_dict = {}

    try:
        # Try to find activity from slug
        activity = Activity.objects.get(slug=activity_name_slug)
        context_dict['activity'] = activity
    except Activity.DoesNotExist:
        context_dict['activity'] = None

    # Make sure activity was found
    if context_dict['activity'] and request.method == 'GET':
        # Get pictures from that activity
        pictures = activity.picture_set.all()

        if pictures.all().count() > 0:
            first_picture = pictures[0] # Separate first picture, due to template requirements
            context_dict["first_picture"] = first_picture
            context_dict["pictures"] = pictures[1:]

    return render(request, 'actifind/show_pictures.html', context_dict)


# Serve a search query and display results
def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "Please enter search keywords"
        return render(request, 'actifind/index.html', {'error_msg': error_msg})

    activity_list = Activity.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(address__icontains=q) | Q(activity_type__icontains=q))
    return render(request, 'actifind/search_results.html', {'error_msg': error_msg, 'activities': activity_list})

# Login user
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

### VIEWS WERE LOGIN IS REQUIRED ###

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# Serve profile page
@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    # Get user profile
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'picture': userprofile.picture, })

    # Process request if a picture was sent
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)

    return render(request, 'actifind/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})


# Process picture uploads and serve form
@login_required
def upload_picture(request, activity_name_slug):
    context_dict = {}

    try:
        # Look for activity slug
        activity = Activity.objects.get(slug=activity_name_slug)
        context_dict['activity'] = activity
    except Activity.DoesNotExist:
        context_dict['activity'] = None

    # Process form if activtiy was found
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

    return render(request, 'actifind/upload_picture.html', context_dict)


# Serve page for showing only reviews of a specific user
@login_required
def show_my_reviews(request):
    context_dict = {}

    # Get user from request and check it has at least one review
    if request.user and request.user.review_set.count() > 0:
        # Initialize paginator object to handle pages
        review_list = request.user.review_set.all().order_by('-id')
        paginator = Paginator(review_list, 10)  # Limit 10 per page
        page = int(request.GET.get('page') or 1) # Get current page, if no page then 1
        reviews = paginator.page(page)
        context_dict['reviews'] = reviews

    return render(request, 'actifind/show_my_reviews.html', context_dict)


# Function to process POST request to add a review
@login_required
def add_review(request):
    activity_slug = None
    review = None

    # Look for activity
    if request.method == 'POST':
        activity_slug = request.POST['activity']
    if activity_slug:
        try:
            # Try to find activity from slug
            activity = Activity.objects.get(slug=activity_slug)
            # Set attributes
            rating = int(request.POST['rating']) 
            title = request.POST['title']
            description = request.POST['description']
            # Save object
            review = Review(title=title, rating=rating, message=description, activity=activity, user=request.user)
            review.save()
        except Activity.DoesNotExist:
            review = None

    return HttpResponse(review)

# Serve page to add activity and process form
@login_required
def add_activity(request):
    form = ActivityForm()
    if request.method == 'POST':
        form = ActivityForm(request.POST)

        # Check form is valid
        if form.is_valid():
            activity = form.save(commit=False)

            # Assign user
            activity.user = request.user

            # Get hidden fields
            activity.lat = float(request.POST['act-lat'])
            activity.lng = float(request.POST['act-lng'])
            activity.save()

            # Process tags assigned if there are any in request
            if request.POST['tags-string']:
                tags = request.POST['tags-string'].split(",")

                # Get or create a new tag with that name
                for tag_name in tags:
                    tag = Tag.objects.get_or_create(name=tag_name)[0]
                    activity.tags.add(tag)  # Add to activity

            return index(request)
        else:
            print(form.errors)

    context_dict = {
        "GOOGLE_MAPS_KEY": settings.GOOGLE_MAPS_KEY,
        "form": form
    }

    return render(request, 'actifind/add_activity.html', context_dict)

