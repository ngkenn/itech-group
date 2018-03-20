import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'itechGroup.settings')

import django
django.setup()
from actifind.models import Activity, Review, User
from dateutil import parser
from datetime import datetime
import random

def populate():
    users = [
        { 
            "username": 'testuser',
            "email": 'test@test.com',
            "password": '12344321'
        },
        { 
            "username": 'jgalvan',
            "email": 'jgalvan@test.com',
            "password": '12344321'
        },
        { 
            "username": 'bestuser',
            "email": 'best@test.com',
            "password": '12344321'
        }
    ]

    running_reviews = [
        {
            "title": "Running at Loch Lomond",
            "date":"22/01/2018",
            "rating":5
        },
        {
            "title": "Running in Kelvingrove Park",
            "date":"17/03/2018",
            "rating":4
        },
        {
            "title":"Running up Buchannan Street",
            "date":"12/3/2018",
            "rating":2
        },
        {
            "title":"Running the Royal Mile",
            "date":"21/2/2018",
            "rating":4
        },
    ]
    cycling_reviews = [
        {
            "title":"Cycling along the Clyde",
            "date":"1/3/18",
            "rating":3
        },
        {
            "title":"Cycling Glasgow City Centre",
            "date":"12/3/2018",
            "rating":2
        },
        {
            "title":"Cycling to Loch Lomond",
            "date":"12/3/2018",
            "rating":4
        },
        {
            "title":"Pollok Park cycling",
            "date":"21/2/2018",
            "rating":5
        },
        {
            "title":"Firth and Clyde Canal path to Kirkintilloch",
            "date":"12/3/2018",
            "rating":5
        },
        {
            "title":"Cathkin Braes Mountain Bike trails",
            "date":"7/3/2018",
            "rating":5
        },
        {
            "title":"Clyde and Loch Lomond Cycleway",
            "date":"8/2/2018",
            "rating":5
        },
    ]
    walking_reviews = [
        {
            "title":"Ben Lomond easy route",
            "date":"28/2/18",
            "rating":4
        },
        {
            "title":"Pollok Country Park",
            "date":"2/3/18",
            "rating":5
        },
        {
            "title":"Linn Park",
            "date":"12/3/18",
            "rating":5
        },
        {
            "title":"The Necropolis",
            "date":"12/3/18",
            "rating":5
        },
        {
            "title":"Glasgow Green",
            "date":"1/2/18",
            "rating":4
        },
        {
            "title":"Bellahouston Park",
            "date":"8/2/18",
            "rating":5
        },
        {
            "title":"Queens Park",
            "date":"12/2/18",
            "rating":5
        },
        {
            "title":"Possil Park",
            "date":"28/2/18",
            "rating":1
        },
    ]

    acts = {
        "Running at Loch Lomond": {
            "activity_type": "Running",
            "description": "Peaceful run",
            "address": "Loch Lomond, United Kingdom",
            "reviews": running_reviews
            },
        "Running in Kelvingrove Park": {
            "activity_type": "Running",
            "description": "Nice park run",
            "address": "Kelvingrove Park, Glasgow, United Kingdom",
            "reviews": running_reviews
            },
        "Running up Buchannan Street": {
            "activity_type": "Running",
            "description": "Running in busy shopping street",
            "address": "Buchannan Street, Glasgow, United Kingdom",
            "reviews": running_reviews
            },
        "Running the Royal Mile": {
            "activity_type": "Running",
            "description": "Scenic run",
            "address": "The Royal Mile, Edinburgh, United Kingdom",
            "reviews": running_reviews
            },
        "Cycling along the Clyde": {
            "activity_type": "Cycling",
            "description": "Wonderful bike ride",
            "address": "River Clyde, UK",
            "reviews": cycling_reviews
            },
        "Walking around Ben Lomond":{
            "activity_type": "Walking",
            "description": "Great walk",
            "address": "Ben Lomond, Stirling, UK",
            "reviews": walking_reviews
            },
        "Pollok Country Park walk":{
            "activity_type": "Walking",
            "description": "Nice quiet park close to the city",
            "address": "Pollok Country Park, Glasgow, UK",
            "reviews": walking_reviews
            },
        "Linn Park stroll":{
            "activity_type": "Walking",
            "description": "Lovely for a walk",
            "address": "Linn Park,Glasgow, UK",
            "reviews": walking_reviews
            },
        "Walking around the Necropolis":{
            "activity_type": "Walking",
            "description": "Very interesting historic walk",
            "address": "Glasgow Necropolis, Glasgow, UK",
            "reviews": walking_reviews
            },
        "Glasgow Green":{
            "activity_type": "Walking",
            "description": "Very nice, People's Palace is also worth a visit",
            "address": "Glasgow Green, Glasgow, UK",
            "reviews": walking_reviews
            },
        "Bellahouston Park walk":{
            "activity_type": "Walking",
            "description": "Lovely park for a walk",
            "address": "Bellahouston Park, Glasgow, UK",
            "reviews": walking_reviews
            },
        "Walking around Queens Park":{
            "activity_type": "Walking",
            "description": "Nice park, cool glass house and lots to do nearby",
            "address": "Queens Park, Glasgow, UK",
            "reviews": walking_reviews
            },
        "Walking around Ben Lomond":{
            "activity_type": "Walking",
            "description": "Great walk",
            "address": "Ben Lomond, Stirling, UK",
            "reviews": walking_reviews
            },
        "Risking my life in Possil Park":{
            "activity_type": "Walking",
            "description": "Very scary walk, felt endangered",
            "address": "Possil Park, Glasgow, UK",
            "reviews": walking_reviews
            }
    }

    for i, user in enumerate(users):
        users[i] = add_user(user['username'], user['email'], user['password'])

    for act, act_data in acts.items():
        a = add_act(act, act_data["activity_type"], act_data["description"], act_data["address"], random.choice(users))
        for r in act_data["reviews"]:
            add_review(a, r["title"], r["date"], r["rating"], random.choice(users))

    for a in Activity.objects.all():
        for r in Review.objects.filter(activity=a):
            print("- {0} - {1}".format(str(a), str(r)))

def add_user(username, email, password):
    u = User.objects.get_or_create(username=username, email=email)[0]
    u.set_password(password)
    u.save()
    return u

def add_review(act, title, date, rating, user):
    r = Review.objects.get_or_create(activity=act, title=title, date=datetime.today(), rating=rating, user=user)[0]
    r.save()
    return r

def add_act(name, activity_type, description, address, user):
    a = Activity.objects.get_or_create(name=name, user=user)[0]
    a.activity_type = activity_type
    a.description = description
    a.address = address
    a.save()
    return a

if __name__ =='__main__':
    print("Starting Actifind population script...")
    populate()
