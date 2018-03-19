from django.test import TestCase
from actifind.models import Review, Activity, Picture, UserProfile
from django.contrib.staticfiles import finders
from django.contrib.auth.models import User
from actifind.forms import ReviewForm, UserForm, UserProfileForm, Activity
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.test.client import Client


class FindLogo(TestCase):
    def test_serving_static_files(self):

        result = finders.find('images/actifind_logo.png')
        self.assertIsNotNone(result)


# class Login(TestCase):
#     def test_for_logging_in(self):
#         self.credentials = {'username' : 'testuser',
#                             #'email': 'tester@gmail.com',
#                             'password': 'secretpass'}
#         User.objects.create_user(**self.credentials)
#
#     def test_login(self):
#         self.credentials = {'username': 'testuser',
#                             # 'email': 'tester@gmail.com',
#                             'password': 'secretpass'}
#
#         user = auth.get_user(self.client)
#
#         self.assertTrue (user.is_authenticated)
#
#         response = self.client.post('register/', self.credentials, follow=True)
#
#         self.assertTrue(response.context['user'].is_active) #not working atm
#


class IndexTests(TestCase):

    def test_index_using_template(self):

        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'actifind/base.html')


class ActivityTest(TestCase):

    def setUp(self):
        Activity.objects.create(name="Photography", description="Great for when the sun is out")
        Activity.objects.create(name="Rock Climbing",description="Good day out with the kids")


    def test_activity_is_present(self):
        #Test to see if inputted data is present
        photography = Activity.objects.get(name="Photography")
        rock_climbing = Activity.objects.get(name="Rock Climbing")

        self.assertEqual(photography.name, "Photography")
        self.assertEqual(rock_climbing.description, "Good day out with the kids")


# class Registration(TestCase):
#
#     def test_authentication(self):
#         response = self.client.post(reverse('index'), {'username': 'tester',
#                                                        'email': 'tester@gmail.com',
#                                                        'password': 'testerpass'})
#
#         user = auth.get_user(self.client)
#
#         c = Client()
#         c.login(username='fred', password='secret')
#
#         #self.assertTrue(user.is_authenticated)
#
#         assert user.is_authenticated

# class UserTest(TestCase):
#
#     def setUp(self):
#         self.client = Client()


class UserTEST(TestCase):
    def test_create_user(self):
        # Create a user
        from actifind.models import UserProfile
        user = UserProfile.objects.get_or_create(username="testuser", password="test1234",
                                           email="testuser@testuser.com")[0]
        user.set_password(user.password)
        user.save()

        return user

        self.assertTrue(user.is_authenticated)

