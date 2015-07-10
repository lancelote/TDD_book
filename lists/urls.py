# pylint: skip-file

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='home'),
    url(r'^lists/(.+)/$', views.view_list, name='view_list'),
    url(r'^lists/new$', views.new_list, name='new_list')
]
