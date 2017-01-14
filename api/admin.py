from django.contrib import admin

# Register your models here.

from .models import *

class HouseholdAdmin(admin.ModelAdmin):
    pass

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
  list_display = ('id','get_name', 'get_amount', 'remainder', 'get_period', 'start_time', 'end_time')
  def get_name(self, obj):
    return obj.masterbudget.name
  def get_amount(self, obj):
    return obj.masterbudget.amount
  def get_period(self, obj):
    return obj.masterbudget.period

@admin.register(MasterBudget)
class MasterBudgetAdmin(admin.ModelAdmin):
  list_display = ('id', 'name',
                  'period', 'amount',
                  'expense_type', 'household', 'user'
                  )

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
  list_display = ('name', 'amount', 'category', 'type', 'budget', 'user', 'time')


admin.site.register(User)
admin.site.register(Household, HouseholdAdmin)
admin.site.register(Category)
