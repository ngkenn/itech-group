import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'itechGroup.settings')

import django
django.setup()
from actifind.models import Activity, Review
from dateutil import parser
from datetime import datetime

def populate():
    running_reviews = [
        {  
            "title": "Running at Loch Lomond",
            "date":"22/01/2018", 
            "rating":5
        }
    ]
    cycling_reviews = [
        {
            "title":"Cycling along the Clyde",
            "date":"1/3/18", 
            "rating":3
        }
    ]
    walking_reviews = [
        { 
            "title":"Ben Lomond easy route",
            "date":"28/2/18", 
            "rating":4
        }
    ]

    acts = {
        "Running at Loch Lomond": {
            "activity_type": "Running",
            "description": "Peaceful run",
            "address": "Loch Lomond, United Kingdom",
            "reviews": running_reviews
            },
        "Cycling along the Clyde": {
            "activity_type": "Cycling",
            "description": "Wonderful bike ride",
            "address": "River Clyde, Glasgow, UK",
            "reviews": cycling_reviews
            },
        "Walking around Ben Lomond":{
            "activity_type": "Walking",
            "description": "Great walk",
            "address": "Ben Lomond, Stirling, UK",
            "reviews": walking_reviews
            }
    }

    for act, act_data in acts.items():
        a = add_act(act, act_data["activity_type"], act_data["description"], act_data["address"])
        for r in act_data["reviews"]:
            add_review(a, r["title"], r["date"], r["rating"])

    for a in Activity.objects.all():
        for r in Review.objects.filter(activity=a):
            print("- {0} - {1}".format(str(a), str(r)))

def add_review(act, title, date, rating):
    r = Review.objects.get_or_create(activity=act, title=title, date=datetime.today(), rating=rating)[0]
    r.save()
    return r

def add_act(name, activity_type, description, address):
    a = Activity.objects.get_or_create(name=name)[0]
    a.activity_type = activity_type
    a.description = description
    a.address = address
    a.save()
    return a

if __name__ =='__main__':
    print("Starting Actifind population script...")
    populate()
