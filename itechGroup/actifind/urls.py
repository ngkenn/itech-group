from django.conf.urls import url
from actifind import views


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^activity/(?P<activity_name_slug>[\w\-]+)/add_review/$',
        views.add_review, name='add_review'),
]
