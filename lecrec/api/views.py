from rest_framework import generics
from api.serializers import RecordListSerializer
from api.models import Record


class RecordList(generics.ListAPIView):
    serializer_class = RecordListSerializer

    def get_queryset(self):
        return Record.objects.all()
