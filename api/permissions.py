from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
      print('this is actually called')
      return obj.user == request.user
