from rest_framework import serializers
from api.models import Record


class RecordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('id', 'user', 'filename', 'text', 'created', )
