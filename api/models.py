from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import DateTimeRangeField
import arrow

class User(AbstractUser):
  household = models.ForeignKey('Household', null=True)

  def __str__(self):
    return self.username

class Household(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name


class Record(models.Model):
  TYPE_CHOICES = (
    ('Personal', 'Personal'),
    ('Household', 'Household')
  )

  def acceptable_categories(self):
    return Category.objects.filter(household = self.household)

  user = models.ForeignKey('User', null=True)
  household = models.ForeignKey('Household', null=True)
  category = models.ForeignKey('Category', null=True, blank=True, default=None)
  amount = models.DecimalField(max_digits=8, decimal_places=2)
  name = models.CharField(max_length=500)
  time = models.DateTimeField()
  updated_at = models.DateTimeField(auto_now = True)
  created_at = models.DateTimeField(auto_now_add= True)
  type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='Personal')
  masterbudget = models.ForeignKey('MasterBudget', null=True, blank=True)
  budget = models.ForeignKey('Budget', null=True, blank=True)

  def clean(self):
    if self.category not in self.acceptable_categories():
      raise ValidationError({
        'category': "Invalid Category: {}".format(self.category)
      })

  def save(self, *args, **kwargs):
    if (self.masterbudget is not None):
      pass
      # set the right budget here
      # if one does not exist, create one
      # if one exists, set it
    super(Record, self).save(*args, **kwargs)


  def __str__(self):
    return '{} - {}'.format(self.name, self.amount)

class Category(models.Model):
  name = models.CharField(max_length=200)
  household = models.ForeignKey('Household', null=True, blank=True)

  def __str__(self):
    return "{} - {}".format(self.household, self.name)


class MasterBudget(models.Model):
  PERIOD_CHOICES = (
    ('Monthly','Monthly'),
    ('Weekly', 'Weekly'),
    ('Daily', 'Daily')
  )
  TYPE_CHOICES = (
    ('Personal', 'Personal'),
    ('Household', 'Household')
  )

  name = models.CharField(max_length=200)
  amount = models.DecimalField(max_digits=8, decimal_places=2)
  household = models.ForeignKey('Household')
  user =  models.ForeignKey('User')
  period = models.CharField(max_length=50, choices=PERIOD_CHOICES, default='Monthly')
  expense_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Personal')

  def __str__(self):
    return self.name



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








