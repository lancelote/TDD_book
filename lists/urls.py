# pylint: skip-file

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='home'),
    url(r'^lists/the-only-list-in-the-world/$', views.view_list,
        name='view_list')
]
