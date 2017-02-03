from django.conf.urls import url
from api.views import (
    UserGetOrCreate,
    RecordListCreate,
    RecordRetrieveDeleteUpdate,
)


app_name = 'api'
urlpatterns = [
    # records
    url(r'^users$', UserGetOrCreate.as_view(), name='user-get-or-create'),
    url(r'^records$', RecordListCreate.as_view(), name='record-list-create'),
    url(r'^records/(?P<pk>[\d]+)$', RecordRetrieveDeleteUpdate.as_view(), name='record-retrieve-update-destroy'),
]
