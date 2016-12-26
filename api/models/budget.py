from django.db import models
import arrow

class Budget(models.Model):
  masterbudget = models.ForeignKey('MasterBudget')
  remainder = models.DecimalField(max_digits=8, decimal_places=2)
  start_time = models.DateTimeField(null=True, blank=True)
  end_time = models.DateTimeField(null=True, blank=True)
  # add in start and end dates for these budgets here.

  def __str__(self):
    return str(self.masterbudget)

  @classmethod
  # create a budget from a master given master budget
  def create_budget(cls,masterbudget):

    span = Budget.get_span(masterbudget.period)
    start_time,end_time = arrow.utcnow().span(span)

    budget = cls(
      masterbudget=masterbudget,
      remainder=masterbudget.amount,
      start_time = start_time.datetime,
      end_time =end_time.datetime
    )
    budget.save()
    return budget

  @staticmethod
  def get_span(period):
    if period == 'Monthly':
      return 'month'
    elif period == 'Weekly':
      return 'week'
    elif period == 'Daily':
      return 'day'
    else:
      raise ValueError("Invalid value for perion: {}".format(period))

  def calculate_remainder(self):
    # this methods get all the records that are attached to this budget,
    # sums them up and sets the remainder value.
    pass
