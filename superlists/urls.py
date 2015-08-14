# pylint: skip-file

from django.conf.urls import include, url
from django.contrib import admin

from lists.views import HomePageView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lists/', include('lists.urls', namespace='lists')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts'))
]
