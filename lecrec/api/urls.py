from django.conf.urls import url
from api.views import RecordList, record_list


app_name = 'api'
urlpatterns = [
    # records
    url(r'^records$', RecordList.as_view(), name='record-list'),
    # url(r'^records$', record_list, name='record-list'),
    # url(r'^reocrds/digits', RetrieveView, name = record)
]
