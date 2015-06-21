# pylint: skip-file

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', include('lists.urls', namespace='lists')),
    url(r'^admin/', include(admin.site.urls)),
]