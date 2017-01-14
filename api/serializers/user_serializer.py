from rest_framework import serializers
from ..models import User

class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ('id', 'auth_token', 'first_name', 'last_name', 'email')
