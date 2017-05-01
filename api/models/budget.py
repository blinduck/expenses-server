from django.db import models
import arrow
from datetime import datetime
import logging
from django.dispatch import receiver
logger = logging.getLogger('django')
from django.db.models.signals import post_save

class Budget(models.Model):
  masterbudget = models.ForeignKey('MasterBudget')
  remainder = models.DecimalField(max_digits=8, decimal_places=2)
  ## start and end times are both stored in utc time.
  start_time = models.DateTimeField(null=True, blank=True)
  end_time = models.DateTimeField(null=True, blank=True)

  def __str__(self):
    return str(self.masterbudget)

  @classmethod
  def active_budgets(cls, user):
    budget_ids = [cls.get_or_create_budget(mb).id
               for mb in user.household.masterbudget_set.all()]
    budgets = Budget.objects.filter(id__in= budget_ids)
    return budgets


  @classmethod
  def get_or_create_budget(cls,masterbudget):
    # todo change the timezone implementation
    # -> save the timezone on the user object, pass it in here
    budget = Budget.current_budget(masterbudget)
    if budget: return budget
    span = Budget.get_span(masterbudget.period)
    start_time,end_time = Budget.get_start_and_end_time('Asia/Singapore', span)
    budget = cls(
      masterbudget=masterbudget,
      remainder=masterbudget.amount,
      start_time = start_time,
      end_time =end_time
    )
    budget.save()
    return budget

  @staticmethod
  def get_start_and_end_time(timezone, span):
    """
    span is like week, month etc.
    """
    return [time.to('UTC').datetime for time in arrow.now(timezone).span(span)]

  @staticmethod
  def get_span(period):
    """
    Converts to span values that the arrow library understands
    """

    if period == 'Monthly':
      return 'month'
    elif period == 'Weekly':
      return 'week'
    elif period == 'Daily':
      return 'day'
    else:
      raise ValueError("Invalid value for perion: {}".format(period))

  @staticmethod
  def current_budget(masterbudget):
    time = arrow.utcnow().datetime
    # find a budget for the masterbudget that is within the time period that
    # a budget is active for.
    budgets = Budget.objects.filter(masterbudget = masterbudget)\
      .filter(start_time__date__lte=time)\
      .filter(end_time__date__gte = time)
    if budgets:
      assert(len(budgets) == 1), "More then 1 active budget found: {}".format(len(budgets))
      return budgets[0]
    else:
      return None

  def calculate_remainder(self):
    # this methods get all the records that are attached to this budget,
    # sums them up and sets the remainder value.
    pass


@receiver(post_save, sender='api.Record')
def update_budget(sender, instance, **kwargs):
  if instance.budget is None:
    return
  budget = instance.budget
  budget.remainder -= instance.amount
  budget.save()


