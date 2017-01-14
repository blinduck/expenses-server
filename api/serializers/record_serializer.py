from rest_framework import serializers
from ..models import Record, MasterBudget, Category

class RecordSerializer(serializers.ModelSerializer):
  masterbudget = serializers.PrimaryKeyRelatedField(
    queryset=MasterBudget.objects.all(), allow_null=True)
  category = serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all(), allow_null=True)
  class Meta:
    model = Record
    fields = ('id','user', 'household', 'category', 'amount', 'name', 'type', 'masterbudget', 'time')

