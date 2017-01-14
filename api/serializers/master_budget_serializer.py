from rest_framework import serializers
from ..models import MasterBudget

class MasterBudgetSerializer(serializers.ModelSerializer):
  class Meta:
    model = MasterBudget
    fields = ('id', 'name', 'amount', 'household', 'user', 'period', 'expense_type')

