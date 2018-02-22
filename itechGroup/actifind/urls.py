from django.conf.urls import url
from actifind import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]