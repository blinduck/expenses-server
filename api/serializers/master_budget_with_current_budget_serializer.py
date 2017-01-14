from rest_framework import serializers
from ..models import MasterBudget, Budget
from . import BudgetSerializer

class MasterBudgetWithCurrentBudgetSerializer(serializers.ModelSerializer):
  current_budget = serializers.SerializerMethodField()

  class Meta:
    model = MasterBudget
    fields = ('id','name', 'expense_type', 'amount', 'period', 'current_budget')

  def get_current_budget(self, obj):
    budget = Budget.get_or_create_budget(obj)
    return BudgetSerializer(budget).data

