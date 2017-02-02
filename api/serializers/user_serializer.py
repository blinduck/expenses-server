from rest_framework import serializers
from ..models import User, Household
import inspect

class UserSerializer(serializers.ModelSerializer):
  household = serializers.StringRelatedField()
  # username = serializers.CharField()
  password = serializers.CharField(required=True, write_only=True)
  auth_token = serializers.CharField(read_only=True)

  class Meta:
    model = User
    # read_only_fields = ('id', 'auth_token', 'username', 'password')
    fields = ('id', 'auth_token',
              'first_name', 'last_name',
              'email', 'household', 'password', 'username')

  def create(self, validated_data):
    household_name = self.initial_data['household']
    household = Household.objects.create(name=household_name)
    user = User(**validated_data)
    user.household = household
    user.set_password(validated_data['password'])
    user.save()
    return user

  def validate(self, attrs):
    if Household.objects.filter(name=self.initial_data['household']).exists():
      raise serializers.ValidationError(
        {'household': "A household with that name already exists"})
    return attrs


  def validate_password(self, value):
    if self.initial_data['password_repeat'] != value:
      raise serializers.ValidationError('Passwords do not match')
    return value




