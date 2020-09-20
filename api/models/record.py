from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum, Q

from .category import Category
from .budget import Budget
import arrow
import logging
from datetime import datetime

logger = logging.getLogger('django')


class Record(models.Model):
    TYPE_CHOICES = (
        ('Personal', 'Personal'),
        ('Household', 'Household')
    )

    def acceptable_categories(self):
        return Category.objects.filter(household=self.household)

    user = models.ForeignKey('User', null=True)
    household = models.ForeignKey('Household', null=True)
    categories = models.ManyToManyField("Category")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    name = models.CharField(max_length=500)
    time = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='Personal')
    masterbudget = models.ForeignKey('MasterBudget', null=True, blank=True)
    budget = models.ForeignKey('Budget', null=True, blank=True)

    def save(self, *args, **kwargs):
        if (self.masterbudget is not None) and self.budget is None:
            self.budget = Budget.get_or_create_budget(self.masterbudget)
        if self.household is None:
            self.household = self.user.household
        record = super(Record, self).save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.name, self.amount)

    @classmethod
    def for_month(cls, user, calendar_year,
                  calendar_month, expense_type='all', household=None):

        records = cls.objects.filter(time__year = calendar_year, time__month=calendar_month)
        if household:
            records = records.filter(household=household)
        if user:
            records = records.filter(user=user)
        if expense_type != 'all':
            records = records.filter(type=expense_type)

        return records

    @classmethod
    def for_current_month(cls, user):
        d = datetime.now()
        return cls.for_month(user, d.year, d.month)

    @classmethod
    # can cache this somewhere
    # update whenever a record is created.
    def monthly_category_summary(cls, user, year, month, expense_type='all'):

        categories = Category.objects.filter(Q(cat_type='Household') | Q(cat_type='Personal', user=user))
        groupedCat = {}
        for cat in categories:
            records = cat.record_set.filter(time__year=2018, time__month=month)
            if expense_type != 'all':
                records = records.filter(type=expense_type)
            groupedCat[cat.name] = records.aggregate(total=Sum('amount'))['total']

        records = cls.objects.filter(time__year=2018, time__month=month, categories=None)
        if expense_type != 'all':
            records = records.filter(type=expense_type)
        groupedCat['Uncategorized'] = records.aggregate(total=Sum('amount'))['total']

        return {k: float(v) for k, v in groupedCat.items() if v}.items()

    @classmethod
    def type_summary(cls, user, year, month):
        summary = {}
        records = cls.for_month(None, year, month, expense_type='all')
        personal_records = records.filter(user=user, type="Personal")
        household_records = records.filter(type="Household")
        summary["Personal"] = personal_records.aggregate(Personal=Sum('amount'))['Personal'] if personal_records else 0
        # summary = personal_records.aggregate(Personal=Sum('amount'))
        summary['Household'] = list(household_records.values('user__username').annotate(total=Sum('amount')))
        return summary

    def handle_category(self):
        pass
