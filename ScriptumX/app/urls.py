"""
Definition of urls for polls viewing and voting.
"""

from django.conf.urls import patterns, url
from app.models import Poll
from app.views import PollListView, PollDetailView, PollResultsView

urlpatterns = patterns('',
    url(r'^$',
        PollListView.as_view(
            queryset=Poll.objects.order_by('-pub_date')[:5],
            context_object_name='latest_poll_list',
            template_name='app/index.html',),
        name='home'),
    url(r'^(?P<pk>\d+)/$',
        PollDetailView.as_view(
            template_name='app/details.html'),
        name='detail'),
    url(r'^(?P<pk>\d+)/results/$',
        PollResultsView.as_view(
            template_name='app/results.html'),
        name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'app.views.vote', name='vote'),

    url(r'^gadget/(?P<gadget_id>\d+)?$', 'app.views.gadget', name='gadget'),

    url(r'^project/(?P<id>\d+)?$', 'app.views.dummy', name='dummy'),
    url(r'^script/(?P<id>\d+)?$', 'app.views.dummy', name='dummy'),
    url(r'^scene/(?P<id>\d+)?$', 'app.views.dummy', name='dummy'),
    url(r'^set/(?P<id>\d+)?$', 'app.views.dummy', name='dummy'),
    url(r'^role/(?P<id>\d+)?$', 'app.views.dummy', name='dummy'),
    url(r'^folk/(?P<id>\d+)?$', 'app.views.dummy', name='dummy'),
    url(r'^sfx/(?P<id>\d+)?$', 'app.views.dummy', name='dummy'),
    url(r'^audio/(?P<id>\d+)?$', 'app.views.dummy', name='dummy'),
    url(r'^schedule/(?P<id>\d+)?$', 'app.views.dummy', name='dummy'),
)
