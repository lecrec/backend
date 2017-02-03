from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.serializers import RecordSerializer, UserSerializer
from api.models import Record
from django.contrib.auth.models import User
import json


class UserGetOrCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        user = None

        # TODO
        # change username to user_id
        # change first_name to user_name

        # if user is exists
        if self.request.user.is_anonymous and \
                'username' in request.data :
            try:
                user = User.objects.get(
                    username=request.data.get('username'),
                )
                serializer = self.serializer_class(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                pass

        # else if user is Authenticated with token
        elif not self.request.user.is_anonymous and self.request.user.username == request.data.get('username'):
            user = self.request.user

        # if user object exists, then return user data
        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return self.create(request, *args, **kwargs)


class RecordListCreate(generics.ListCreateAPIView):
    serializer_class = RecordSerializer

    def get_queryset(self):
        print("call!!")
        if self.request.user.is_anonymous:
            return Record.objects.all()
        else:
            return Record.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )

    def post(self, request, *args, **kwargs):
        from api.transcribe import async_transcribe
        from api.wav import wav_split
        from lecrec.settings import MEDIA_ROOT

        if 'voice' in request.FILES:
            request.data['file'] = request.FILES['voice']
        if 'title' in request.data:
            request.data['title'] = request.data['title'].replace('"', '')
        if 'duration' in request.data:
            request.data['duration'] = request.data['duration'].replace('"', '')
        if 'filename' in request.data:
            request.data['filename'] = request.data['filename'].replace('"', '')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # transcribe
        filename = str(request.data.get('file'))
        filepath = MEDIA_ROOT + "/" + filename

        start_times = wav_split(filepath, filename)
        tups = async_transcribe(filename, start_times)

        result = []
        for tup in tups:
            result.append(
                {'time': tup[1], 'text': tup[0]}
            )

        record = Record.objects.get(id=serializer.data.get('id'))
        record.text = json.dumps(result)
        record.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RecordRetrieveDeleteUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
