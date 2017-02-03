from rest_framework import generics, permissions
from api.serializers import RecordSerializer, UserSerializer
from api.models import Record
from django.contrib.auth.models import User
from api.permissions import IsOwnerOrReadOnly

class RecordList(generics.ListCreateAPIView):
    serializer_class = RecordSerializer
    def get_queryset(self):
        return Record.objects.all()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly)


def record_list(request):
    print("here" * 100)
    if request.method == 'GET':
        records = Record.objects.all()
        serializer = RecordListSerializer(records, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RecordListSerializer(data=data)
        #if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data, status=201)
        # return JSONResponse(serializer.errors, status=400)    