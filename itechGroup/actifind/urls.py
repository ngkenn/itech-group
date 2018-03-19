from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from actifind import views
from django.conf import settings
from django.conf.urls.static import static #importing static for URLs

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_activity/$', views.add_activity, name='add_activity'),
    url(r'^activity/(?P<activity_name_slug>[\w\-]+)/$', views.show_activity, name='show_activity'),
    url(r'^register/$', views.register, name='register'),
  #  url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^activity/(?P<activity_name_slug>[\w\-]+)/add_review/$',
        views.add_review, name='add_review'),
    url(r'^upload_picture/$', views.upload_picture, name='upload_picture'),
    url(r'^search/$', views.search, name='search'),



]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
