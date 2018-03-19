from django import template

register = template.Library()

@register.inclusion_tag('actifind/rating.html')
def show_stars(rating, show_rating=False):
    context_dict = {}

    if(rating != 'No rating'):
        half_star = False

        if( (rating%1) > 0.25 and (rating%1) < 0.75 ):
            stars = int(rating)
            missing_stars = 5 - stars - 1
            half_star = True
            rating = int(rating) + 0.5
        else:
            stars = int(round(rating))
            missing_stars = 5 - stars
            rating = stars

        context_dict = {
            "filled_stars": range(0,stars),
            "non_filled_stars": range(0, missing_stars),
            "half_star": half_star
        }

        if(show_rating):
            context_dict['rating'] = rating

    return context_dict

@register.inclusion_tag('actifind/add_review_modal.html')
def add_review_modal():
    return None