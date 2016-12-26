from django.contrib import admin

# Register your models here.

from .models import *

class HouseholdAdmin(admin.ModelAdmin):
    pass

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
  list_display = ('get_name', 'get_amount', 'remainder', 'start_time', 'end_time')
  def get_name(self, obj):
    return obj.masterbudget.name
  def get_amount(self, obj):
    return obj.masterbudget.amount

admin.site.register(User)
admin.site.register(Household, HouseholdAdmin)
admin.site.register(Category)
admin.site.register(Record)
admin.site.register(MasterBudget)
