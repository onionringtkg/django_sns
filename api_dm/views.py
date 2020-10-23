from rest_framework import authentication, permissions
from api_dm import serializers
from core.models import Message
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

#DMのviewset
class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(sender=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Delete is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Update is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'Patch is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

#自分宛のDMを取得するViewset。genericsのListAPIViewも使用可能
class InboxListView(viewsets.ReadOnlyModelViewSet):

    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user)