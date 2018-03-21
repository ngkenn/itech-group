from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from actifind import views
from django.conf import settings
from django.conf.urls.static import static #importing static for URLs

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_activity/$', views.add_activity, name='add_activity'),
    url(r'^activity/(?P<activity_name_slug>[\w\-]+)/$', views.show_activity, name='show_activity'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^activity/(?P<activity_name_slug>[\w\-]+)/upload_picture/$', views.upload_picture, name='upload_picture'),
    url(r'^search/$', views.search, name='search'),
    url(r'^add_review/$', views.add_review, name='add_review'),
    url(r'^activity/(?P<activity_name_slug>[\w\-]+)/show_pictures/$', views.show_pictures, name='show_pictures'),
    url(r'^my_reviews/$', views.show_my_reviews, name='show_my_reviews'),


]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
