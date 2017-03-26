from django.conf.urls import include, url

from talkapp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^users/create/$', views.user_create, name='user_create'),
    url(r'^users/store/$', views.user_store, name='user_store'),
    url(r'^users/edit/$', views.user_edit, name='user_edit'),
    url(r'^users/update/$', views.user_update, name='user_update'),

    url(r'^posts/$', views.post_index, name='post_index'),
    url(r'^posts/create/$', views.post_create, name='post_create'),
    url(r'^posts/store/$', views.post_store, name='post_store'),
    url(r'^posts/(?P<id>\d+)/$', views.post_show, name='post_show'),
    url(r'^posts/(?P<id>\d+)/destroy$', views.post_destroy, name='post_destroy'),

    url(r'^posts/(?P<post_id>\d+)/comments/create/$', views.comment_create, name='comment_create'),
    url(r'^posts/(?P<post_id>\d+)/comments/store/$', views.comment_store, name='comment_store'),

    url(r'^getlogin/$', views.getLogin, name='getlogin'),
    url(r'^postlogin/$', views.postLogin, name='postlogin'),
    url(r'^getlogout/$', views.getLogout, name='getlogout'),
]
