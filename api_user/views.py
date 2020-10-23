from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from api_user import serializers
from core.models import Profile, FriendRequest
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from core import custompermissions

#genericsとModelViewSetを使用する場合がある。
#ModelViewSetはdefaultで全部使用できる（CRUD）
#genericsはCreateAPIViewならcreateのみやってくれる。用途毎に分ける。

# ユーザの新規作成ビュー
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


# 友達申請のviewset
class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.object.all()
    serializer_class = serializers.FriendRequestSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    # ログイン者のみが閲覧可能にする
    permission_classes = (permissions.IsAuthenticated,)

    # 取得
    def get_queryset(self):
        return self.queryset.filter(Q(askTo=self.request.user) | Q(askFrom=self.request.user))

    # 申請時にaskFromをログインしているユーザにするように設定
    def perform_create(self, serializer):
        try:
            serializer.save(askFrom=self.request.user)
        except:
            raise ValidationError("User can have only unique request")

    #削除や部分更新はできなくする（使用不可にしたいときには、以下のようにoverwriteする）
    def destroy(self, request, *args, **kwargs):
        response = {'message': 'delete is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'delete is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializers
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, custompermissions.ProfilePermission)

    #新規作成はログイン後に可能、userProには常にログインしているユーザを割り当てる。
    def perform_create(self, serializer):
        serializer.save(userPro=self.request.user)

#
class MyProfileListView(generics.ListAPIView):

    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializers
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    #ログインしているユーザに基づいたprofileを取得する
    def get_queryset(self):
        return self.queryset.filter(userPro=self.request.user)
