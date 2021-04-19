from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^ToDoList$', views.ToDoItem),
    url(r'^remove/(?P<ToDoItem_id>\d+)$', views.remove),
    url(r'^grant/(?P<ToDoItem_id>\d+)$', views.grant),
    url(r'^ToDoList/edit/(?P<ToDoItem_id>\d+)$', views.edit),
    url(r'^editToDoItem/(?P<ToDoItem_id>\d+)$', views.editToDoItem),
    url(r'^ToDoList/new$', views.newToDoItem),
    url(r'^createtoditem$', views.createToDoItem),
    url(r'^logout$', views.logout)
]