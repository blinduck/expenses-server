from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum

from .category import Category
from .budget import Budget
import arrow
import logging
from datetime import datetime

logger = logging.getLogger('django')


class Record(models.Model):
    # when querying for record list, i hard coded that this are the possible types.
    # when switching to foreignkey types, change that as well
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

    # def clean(self):
    #     if self.categories is not None and self.categories not in self.acceptable_categories():
    #         raise ValidationError({
    #             'category': "Invalid Category: {}".format(self.category)
    #         })

    def save(self, *args, **kwargs):
        logger.info('save called')
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

        # get a time range
        span = [
            d.datetime for d in arrow.Arrow(
                calendar_year, calendar_month, 1
            ).span('month')
        ]
        records = cls.objects.filter(
            time__range=span
        )
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
        print("expense type", expense_type)
        records = cls.for_month(user, year, month, expense_type)
        groupedCat = {}
        for r in records:
            if not r.categories.exists():
                groupedCat['Uncategorized'] = groupedCat.get('Uncategorized', 0) + r.amount
                continue
            for cat in r.categories.all():
                groupedCat[cat.name] = groupedCat.get('cat.name', 0) + r.amount
        return {k: float(v) for k, v in groupedCat.items()}.items()

    @classmethod
    def type_summary(cls, user, year, month):
        records = cls.for_month(None, year, month, expense_type='all')
        personal_records = records.filter(user=user, type="Personal")
        household_records = records.filter(type="Household")
        summary = personal_records.aggregate(Personal=Sum('amount'))
        summary['Household'] = list(household_records.values('user__username').annotate(total=Sum('amount')))
        return summary

    def handle_category(self):
        pass
