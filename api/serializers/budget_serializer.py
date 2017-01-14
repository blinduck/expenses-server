from rest_framework import serializers
from ..models import Budget

class BudgetSerializer(serializers.ModelSerializer):
  class Meta:
    model = Budget
    fields = ('remainder', 'start_time', 'end_time')

