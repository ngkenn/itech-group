import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'itechGroup.settings')

import django
django.setup()
from actifind.models import Activity, Review

def populate():
    running_reviews = [
        {"title": "Running at Loch Lomond",
        "date":"22/01/2018", "rating":5}
    ]
    cycling_reviews = [
        {"title":"Cycling along the Clyde",
        "date":"1/3/18", "rating":3}
    ]
    walking_reviews = [
        {"title":"Ben Lomond easy route",
        "date":"28/2/18", "rating":4}
    ]

    acts={"Running":{"reviews":running_reviews},
    "Cycling":{"reviews":cycling_reviews},
    "Walking":{"reviews":walking_reviews}}

    for act, act_data in acts.items():
        a = add_act(act, description, type)
        for r in act_data["reviews"]:
            add_review(a, r["title"], r["date"], r["rating"])

    for a in Activity.objects.all():
        for r in Review.objects.filter(activity=a):
            print("- {0} - {1}".format(str(c), str(p)))

def add_review(act, title, url, views):
    r = Review.objects.get_or_create(activity=act, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_act(name, type, description):
    a = Activity.objects.get_or_create(name=name, description=null, type=null)
    a.save()
    return a

if __name__ =='__main__':
    print("Starting Actifind population script...")
    populate()
