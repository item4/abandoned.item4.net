from django.conf.urls import url

from .viewsets import UserViewSet


urlpatterns = [
    url(r'^(?P<pk>.+)/$', UserViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    })),
]
