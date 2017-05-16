from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^mode/(?P<mode>\w+)$', set_mode, name='set-mode'),
    url(r'^(?P<hash>\w+)/$', checkin, name='check-in'),
    url(r'$', checkin, name='check-in')
]
