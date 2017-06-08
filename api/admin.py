from django.contrib import admin

# Register your models here.

from .models import *


class UserInline(admin.StackedInline):
    model = User
    fields = ('username',)
    extra = 0


class HouseholdAdmin(admin.ModelAdmin):
    inlines = [
        UserInline
    ]


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_name', 'get_amount',
        'remainder', 'get_period',
        'start_time', 'end_time',
    )

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
    list_display = ('name', 'amount', 'type', 'budget', 'user', 'time')
    list_filter = ("household",)
    date_hierarchy = 'time'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'token')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'household', 'cat_type', 'user')
    list_editable =('cat_type', 'user')


admin.site.register(Household, HouseholdAdmin)
