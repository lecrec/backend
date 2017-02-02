from django.conf.urls import url
from api.views import RecordList


app_name = 'api'
urlpatterns = [
    # records
    url(r'^records$', RecordList.as_view(), name='record-list'),
]