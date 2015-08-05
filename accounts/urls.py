# pylint: skip-file

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$$', views.persona_login, name='persona_login')
]
