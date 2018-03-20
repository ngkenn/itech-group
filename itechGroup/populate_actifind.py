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
        },
        {
            "username": 'superrunner',
            "email": 'runner@test.com',
            "password": '12344321'
        },
        {
            "username": 'wondersports',
            "email": 'sporty@test.com',
            "password": '12344321'
        },
        {
            "username": 'outdoorsman',
            "email": 'outy@test.com',
            "password": '12344321'
        },
        {
            "username": 'mrssports',
            "email": 'mrssports@test.com',
            "password": '12344321'
        },
        {
            "username": 'icanruntoo',
            "email": 'icanrun@test.com',
            "password": '12344321'
        },
        {
            "username": 'gooutside',
            "email": 'outsdie@test.com',
            "password": '12344321'
        },
        {
            "username": 'outsidewoman',
            "email": 'bethere@test.com',
            "password": '12344321'
        },
    ]


    running_at_loch_lomond_reviews =[
        {
            "title":"Great place for a run, will definitely be back",
            "date":"20/2/18",
            "rating":5,
            "user": "jgalvan"
        },
        {
            "title":"Wonderful",
            "date":"20/2/18",
            "rating":5,
            "user": "superrunner"
        },
    ]

    Running_in_Kelvingrove_Park_reviews =[
        {
            "title":"beautiful",
            "date":"20/2/18",
            "rating":5,
            "user": "bestuser"
        },
        {
            "title":"Wonderful",
            "date":"20/2/18",
            "rating":4,
            "user": "wondersports"
        },
        {
            "title":"Very good",
            "date":"20/2/18",
            "rating":5,
            "user": "outdoorsman"
        },
        {
            "title":"Lovely jubbly",
            "date":"20/2/18",
            "rating":5,
            "user": "mrssports"
        },
    ]

    Running_the_Royal_Mile_reviews =[
        {
            "title":"Awe Inspiring",
            "date":"20/2/18",
            "rating":5,
            "user": "wondersports"
        },
        {
            "title":"Wonderful",
            "date":"20/2/18",
            "rating":5,
            "user": "superrunner"
        },
        {
            "title":"Makes me feel so Scottish it hurts",
            "date":"20/2/18",
            "rating":5,
            "user": "jgalvan"
        },
        {
            "title":"Wonderful",
            "date":"20/2/18",
            "rating":5,
            "user": "mrssports"
        },
    ]

    Running_up_Buchannan_Street_reviews =[
        {
            "title":"Bit too busy for me",
            "date":"20/2/18",
            "rating":2,
            "user": "jgalvan"
        },
        {
            "title":"Some strange people around",
            "date":"20/2/18",
            "rating":3,
            "user": "superrunner"
        },
        {
            "title":"Better than Edinburgh",
            "date":"20/2/18",
            "rating":4,
            "user": "mrssports"
        },
        {
            "title":"I like running",
            "date":"20/2/18",
            "rating":3,
            "user": "icanruntoo"
        },
    ]
    Cycling_along_the_Clyde_reviews =[
        {
            "title":"beautiful",
            "date":"20/2/18",
            "rating":5,
            "user": "jgalvan"
        },
        {
            "title":"Wonderful",
            "date":"20/2/18",
            "rating":5,
            "user": "wondersports"
        },
        {
            "title":"Just get outside dudez n dudettez",
            "date":"20/2/18",
            "rating":5,
            "user": "gooutside"
        },
        {
            "title":"Incredible",
            "date":"20/2/18",
            "rating":5,
            "user": "superrunner"
        },
    ]
    Walking_around_Ben_Lomond_reviews =[
        {
            "title":"Mountains hmmm nice",
            "date":"20/2/18",
            "rating":5,
            "user": "jgalvan"
        },
        {
            "title":"Wonderful",
            "date":"20/2/18",
            "rating":5,
            "user": "superrunner"
        },
    ]
    Pollok_Country_Park_walk_reviews =[
        {
            "title":"Fresh air at last",
            "date":"20/2/18",
            "rating":5,
            "user": "outdoorsman"
        },
        {
            "title":"Superdooper",
            "date":"20/2/18",
            "rating":4,
            "user": "superrunner"
        },
    ]
    Linn_Park_stroll_reviews =[
        {
            "title":"Quite nice",
            "date":"20/2/18",
            "rating":4,
            "user": "jgalvan"
        },
        {
            "title":"How lovely",
            "date":"20/2/18",
            "rating":5,
            "user": "outsidewoman"
        },
    ]
    Walking_around_the_Necropolis_reviews =[
        {
            "title":"How old and nice",
            "date":"20/2/18",
            "rating":5,
            "user": "jgalvan"
        },
        {
            "title":"So historic",
            "date":"20/2/18",
            "rating":5,
            "user": "superrunner"
        },
        {
            "title":"Inspirational",
            "date":"20/2/18",
            "rating":5,
            "user": "icanruntoo"
        },
        {
            "title":"Good when the weather is nice",
            "date":"20/2/18",
            "rating":4,
            "user": "outsidewoman"
        },
        {
            "title":"Too urban for me",
            "date":"20/2/18",
            "rating":3,
            "user": "gooutside"
        },
        {
            "title":"Old as you get round here",
            "date":"20/2/18",
            "rating":5,
            "user": "wondersports"
        }
    ]
    Glasgow_Green_reviews =[
        {
            "title":"Wonderful in the sun",
            "date":"20/2/18",
            "rating":5,
            "user": "wondersports"
        },
        {
            "title":"Lovely",
            "date":"20/2/18",
            "rating":5,
            "user": "superrunner"
        },
    ]

    Bellahouston_Park_walk_reviews =[
        {
            "title":"Nice",
            "date":"20/2/18",
            "rating":4,
            "user": "jgalvan"
        },
        {
            "title":"Cool",
            "date":"20/2/18",
            "rating":3,
            "user": "superrunner"
        },
    ]

    Glasgow_Green_reviews =[
        {
            "title":"Wonderful in the sun",
            "date":"20/2/18",
            "rating":5,
            "user": "mrssports"
        },
        {
            "title":"Lovely",
            "date":"20/2/18",
            "rating":3,
            "user": "superrunner"
        },
        {
            "title":"Nice for a chilled day",
            "date":"20/2/18",
            "rating":4,
            "user": "icanruntoo"
        },
        {
            "title":"Lovely",
            "date":"20/2/18",
            "rating":5,
            "user": "gooutside"
        },
    ]

    Walking_around_Queens_Park_reviews =[
        {
            "title":"Number 1 in the southside",
            "date":"20/2/18",
            "rating":5,
            "user": "jgalvan"
        },
        {
            "title":"Really nice",
            "date":"20/2/18",
            "rating":5,
            "user": "superrunner"
        },
    ]

    Walking_around_Ben_Lomond_reviews =[
        {
            "title":"Amazing day out",
            "date":"20/2/18",
            "rating":5,
            "user": "jgalvan"
        },
        {
            "title":"Lovely",
            "date":"20/2/18",
            "rating":5,
            "user": "superrunner"
        },
        {
            "title":"So authentic",
            "date":"20/2/18",
            "rating":5,
            "user": "icanruntoo"
        },
        {
            "title":"Lovely",
            "date":"20/2/18",
            "rating":5,
            "user": "gooutside"
        },
    ]

    Risking_my_life_in_Possil_Park_reviews =[
        {
            "title":"Traumatic experience, I was almost killed by a ned",
            "date":"20/2/18",
            "rating":1,
            "user": "jgalvan"
        },
        {
            "title":"Terrible, chased a guy to try and give him back his wallet for an hour and he called the police saying I was trying to kill him",
            "date":"20/2/18",
            "rating":1,
            "user": "superrunner"
        },
    ]


    acts = {
        "Running at Loch Lomond": {
            "activity_type": "Running",
            "description": "Peaceful run",
            "address": "Loch Lomond, United Kingdom",
            "reviews": running_at_loch_lomond_reviews,
            "user": "superrunner"
            },
        "Running in Kelvingrove Park": {
            "activity_type": "Running",
            "description": "Nice park run",
            "address": "Kelvingrove Park, Glasgow, United Kingdom",
            "reviews": Running_in_Kelvingrove_Park_reviews,
            "user": "jgalvan"
            },
        "Running up Buchannan Street": {
            "activity_type": "Running",
            "description": "Running in busy shopping street",
            "address": "Buchannan Street, Glasgow, United Kingdom",
            "reviews": Running_up_Buchannan_Street_reviews,
            "user": "gooutside"
            },
        "Running the Royal Mile": {
            "activity_type": "Running",
            "description": "Scenic run",
            "address": "The Royal Mile, Edinburgh, United Kingdom",
            "reviews": Running_the_Royal_Mile_reviews,
            "user": "icanruntoo"
            },
        "Cycling along the Clyde": {
            "activity_type": "Cycling",
            "description": "Wonderful bike ride",
            "address": "River Clyde, UK",
            "reviews": Cycling_along_the_Clyde_reviews,
            "user": "jgalvan"
            },
        "Walking around Ben Lomond":{
            "activity_type": "Walking",
            "description": "Great walk",
            "address": "Ben Lomond, Stirling, UK",
            "reviews": Walking_around_Ben_Lomond_reviews,
            "user": "jgalvan"
            },
        "Pollok Country Park walk":{
            "activity_type": "Walking",
            "description": "Nice quiet park close to the city",
            "address": "Pollok Country Park, Glasgow, UK",
            "reviews": Pollok_Country_Park_walk_reviews,
            "user": "icanruntoo"
            },
        "Linn Park stroll":{
            "activity_type": "Walking",
            "description": "Lovely for a walk",
            "address": "Linn Park,Glasgow, UK",
            "reviews": Linn_Park_stroll_reviews,
            "user": "icanruntoo"
            },
        "Walking around the Necropolis":{
            "activity_type": "Walking",
            "description": "Very interesting historic walk",
            "address": "Glasgow Necropolis, Glasgow, UK",
            "reviews": Walking_around_the_Necropolis_reviews,
            "user": "icanruntoo"
            },
        "Glasgow Green":{
            "activity_type": "Walking",
            "description": "Very nice, People's Palace is also worth a visit",
            "address": "Glasgow Green, Glasgow, UK",
            "reviews": Glasgow_Green_reviews,
            "user": "icanruntoo"
            },
        "Bellahouston Park walk":{
            "activity_type": "Walking",
            "description": "Lovely park for a walk",
            "address": "Bellahouston Park, Glasgow, UK",
            "reviews": Bellahouston_Park_walk_reviews,
            "user": "jgalvan"
            },
        "Walking around Queens Park":{
            "activity_type": "Walking",
            "description": "Nice park, cool glass house and lots to do nearby",
            "address": "Queens Park, Glasgow, UK",
            "reviews": Walking_around_Queens_Park_reviews,
            "user": "gooutside"
            },
        "Walking around Ben Lomond":{
            "activity_type": "Walking",
            "description": "Great walk",
            "address": "Ben Lomond, Stirling, UK",
            "reviews": Walking_around_Ben_Lomond_reviews,
            "user": "icanruntoo"
            },
        "Risking my life in Possil Park":{
            "activity_type": "Walking",
            "description": "Very scary walk, felt endangered",
            "address": "Possil Park, Glasgow, UK",
            "reviews": Risking_my_life_in_Possil_Park_reviews,
            "user": "gooutside"
            }
    }

    for i, user in enumerate(users):
        users[i] = add_user(user['username'], user['email'], user['password'])

    for act, act_data in acts.items():
        a = add_act(act, act_data["activity_type"], act_data["description"], act_data["address"], act_data["user"])
        for r in act_data["reviews"]:
            add_review(a, r["title"], r["date"], r["rating"], r["user"])

    for a in Activity.objects.all():
        for r in Review.objects.filter(activity=a):
            print("- {0} - {1}".format(str(a), str(r)))

def add_user(username, email, password):
    u = User.objects.get_or_create(username=username, email=email)[0]
    u.set_password(password)
    u.save()
    return u

def add_review(act, title, date, rating, user):
    u = User.objects.get(username=user)
    r = Review.objects.get_or_create(activity=act, title=title, rating=rating, user=u)[0]
    r.save()
    return r

def add_act(name, activity_type, description, address, username):
    u = User.objects.get(username=username)
    a = Activity.objects.get_or_create(name=name, user=u)[0]
    a.activity_type = activity_type
    a.description = description
    a.address = address
    a.save()
    return a

if __name__ =='__main__':
    print("Starting Actifind population script...")
    populate()
