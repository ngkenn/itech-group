# Functions that will be used as template tags
# to render partial parts of the page
from django import template

register = template.Library()

# Gets rating and processes it to show it in a suitable way
@register.inclusion_tag('actifind/rating.html')
def show_stars(rating, show_rating=False):
    context_dict = {}

    if(rating != 'No rating'):
        half_star = False

        # Check if rating is within threshold to show half star
        if( (rating%1) > 0.25 and (rating%1) < 0.75 ):
            stars = int(rating) # amount of stars to be shown
            missing_stars = 5 - stars - 1   # amount of empty stars to be shown
            half_star = True    # half star
            rating = int(rating) + 0.5
        else: 
            stars = int(round(rating)) # amount of stars to be shown
            missing_stars = 5 - stars # amount of empty stars to be shown
            rating = stars

        context_dict = {
            "filled_stars": range(0,stars),
            "non_filled_stars": range(0, missing_stars),
            "half_star": half_star
        }

        if(show_rating):
            context_dict['rating'] = rating

    return context_dict

# Function to process call to template tag add review modal
@register.inclusion_tag('actifind/add_review_modal.html')
def add_review_modal():
    return None

# Function to process call to template tag show_reviews
@register.inclusion_tag('actifind/show_reviews.html')
def show_reviews(reviews, include_links=False):
    context_dict = {
        "reviews": reviews,
        "include_links": include_links
    }
    return context_dict

# Function to process call to template tag show activity list
@register.inclusion_tag('actifind/activity_list.html')
def show_activity_list(activities):
    return { "activities": activities }