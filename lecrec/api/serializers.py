from rest_framework import serializers
from api.models import Record
from django.contrib.auth.models import User
import time


class RecordSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField(readonly=True)
    # user = serializers.PrimaryKeyRelatedField(many=True)
    user = serializers.ReadOnlyField(source='user.username')
    text = serializers.CharField(required=False)
    filename = serializers.CharField(required=False)
    class Meta:
        model = Record
        fields = ('id', 'filename', 'text', 'created', 'user',) #
    # def perform_create(self, serializer):
    #     user = User.objects.get(username=request.data['username'])
    #     serializer.save()
        # print('\n' * 10)
        # print(user)
        # with open('../media/' + filename, 'wb') as f:
        #     f.write(request.FILES['wav'][1])
        # serializer.save(id=self.id, user=int(user.pk),
        #     filename=filename, text='dummy', created=self.created)



class UserSerializer(serializers.ModelSerializer):
    records = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Record.objects.all())
    class Meta:
        model = User
        fields = ('username', 'password')
    # def perform_create(self, serializer):
    #     serializer.save(
    #         username=self.request.POST['username'],
    #         password=self.request.POST['password'],
    #         )