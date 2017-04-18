from django.conf.urls import url

from .views import ExpansionList, ExpansionDetail, ArtistList, ArtistDetail

urlpatterns = [
    url(r'^exp/$', ExpansionList.as_view(), name='expansion-list'),
    url(r'^exp/(?P<code>[_a-zA-Z0-9]{3,9})/$', ExpansionDetail.as_view(), name='expansion-detail'),

    url(r'^art/$', ArtistList.as_view(), name='artist-list'),
    url(r'^art/(?P<pk>\d+)/$', ArtistDetail.as_view(), name='artist-detail'),
]
