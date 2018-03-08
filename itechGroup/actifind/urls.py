from django.conf.urls import url
from actifind import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_activity/$', views.add_activity, name='add_activity'),
    url(r'^activity/(?P<activity_name_slug>[\w\-]+)/$', views.show_activity, name='show_activity'),
]