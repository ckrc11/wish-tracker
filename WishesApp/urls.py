from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^wishes$', views.wishes),
    url(r'^remove/(?P<wish_id>\d+)$', views.remove),
    url(r'^grant/(?P<wish_id>\d+)$', views.grant),
    url(r'^wishes/edit/(?P<wish_id>\d+)$', views.edit),
    url(r'^editwish/(?P<wish_id>\d+)$', views.editwish),
    url(r'^wishes/new$', views.newWish),
    url(r'^createwish$', views.createwish),
    url(r'^logout$', views.logout)
]