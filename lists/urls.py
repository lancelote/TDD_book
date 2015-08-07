# pylint: skip-file

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(\d+)/$', views.view_list, name='view_list'),
    url(r'^new$', views.new_list, name='new_list'),
    url(r'^users/(.+)/$', views.my_lists, name='my_lists')
]
