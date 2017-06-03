from rest_framework import serializers
from ..models import Record, MasterBudget, Category

class RecordCreateSerializer(serializers.ModelSerializer):
  masterbudget = serializers.PrimaryKeyRelatedField(
    queryset=MasterBudget.objects.all(), allow_null=True)
  class Meta:
    model = Record
    fields = ('id','user', 'household', 'categories', 'amount', 'name', 'type', 'masterbudget', 'time')


class RecordListSerializer(serializers.ModelSerializer):
  masterbudget = serializers.PrimaryKeyRelatedField(
    queryset=MasterBudget.objects.all(), allow_null=True)
  category = serializers.StringRelatedField()
  class Meta:
    model = Record
    fields = ('id','user', 'household', 'category',
              'amount', 'name', 'type',
              'masterbudget', 'time')
