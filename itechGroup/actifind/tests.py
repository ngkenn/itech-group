from django.test import TestCase
from actifind.models import Review, Activity, Picture, UserProfile
from django.contrib.staticfiles import finders
from django.contrib.auth.models import User
from actifind.forms import UserForm, UserProfileForm, Activity
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.test.client import Client


class FindLogo(TestCase):
    def test_serving_static_files(self):

        result = finders.find('images/actifind_logo.png')
        self.assertIsNotNone(result)


class IndexTests(TestCase):

    def test_index_using_template(self):

        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'actifind/base.html')


class ActivityTest(TestCase):

    def setUp(self):
        #Passing a user_id as the field User cannot be null
        Activity.objects.create(name="Photography", description="Great for when the sun is out", user_id='4')

        Activity.objects.create(name="Rock Climbing",description="Good day out with the kids", user_id='3')


    def test_activity_is_present(self):
        #Test to see if inputted data is present user needs a user ID
        photography = Activity.objects.get(name="Photography")
        rock_climbing = Activity.objects.get(name="Rock Climbing")

        self.assertEqual(photography.name, "Photography")
        self.assertEqual(rock_climbing.description, "Good day out with the kids")


class LoginTest(TestCase):

    def setUp(self):
        #Create a user
        user = User.objects.create_user(username='tester')
        user.set_password('er123')
        user.save()

    def test_log(self):
        #test to see if it is possible to log in
        c = Client()
        logged_in = c.login(username='tester', password='er123')
        self.assertTrue(logged_in)



class ModelTest(TestCase):

    #Unit test for review model

    def create_Review(self, title='Glasgow', rating='3', message='Very busy', activity_id='6', user_id='8'):
        return Review.objects.create(title=title, rating=rating, message=message,activity_id=activity_id, user_id=user_id)

    def test_review_creation(self):
        r = self.create_testReview()

        self.assertTrue(isinstance(r, Review))
        self.assertEqual(r.__str__(), r.title)
