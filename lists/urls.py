# pylint: skip-file

from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /
    url(
        r'^$',
        views.homepage,
        name='home'),
]
