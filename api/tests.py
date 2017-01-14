from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .models import *


# Create your tests here.

class BudgetTestCase(TestCase):
  fixtures = ['users.json', 'households.json', 'master_budgets.json']

  def test_budget_is_created_if_it_does_not_exist(self):
    assert len(Budget.objects.all()) == 0
    for mb in MasterBudget.objects.all():
      Budget.get_or_create_budget(mb)
    assert len(Budget.objects.all()) == 3

    for mb in MasterBudget.objects.all():
      Budget.get_or_create_budget(mb)
    assert len(Budget.objects.all()) == 3


