from rest_framework import permissions


# プロフィールの更新や削除は、ログインしているユーザのみが行えるようにする。

class ProfilePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.userPro.id == request.user.id
