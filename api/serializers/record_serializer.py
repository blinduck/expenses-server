from rest_framework import serializers
from ..models import Record, MasterBudget, Category

class RecordCreateSerializer(serializers.ModelSerializer):
  masterbudget = serializers.PrimaryKeyRelatedField(
    queryset=MasterBudget.objects.all(), allow_null=True)
  categories = serializers.PrimaryKeyRelatedField(many=True, allow_empty=True, queryset=Category.objects.all())
  class Meta:
    model = Record
    fields = ('id','user', 'household', 'categories', 'amount', 'name', 'type', 'masterbudget', 'time')


class RecordListSerializer(serializers.ModelSerializer):
  masterbudget = serializers.PrimaryKeyRelatedField(
    queryset=MasterBudget.objects.all(), allow_null=True)
  class Meta:
    model = Record
    fields = ('id','user', 'household', 'categories',
              'amount', 'name', 'type',
              'masterbudget', 'time')
