from django.db import models
from django.core.exceptions import ValidationError
from .category import Category
from .budget import Budget
import logging
logger = logging.getLogger('django')

class Record(models.Model):
  #when querying for record list, i hard coded that this are the possible types.
  # when switching to foreignkey types, change that as well
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
    if self.category is not None and self.category not in self.acceptable_categories():
      raise ValidationError({
        'category': "Invalid Category: {}".format(self.category)
      })

  def save(self, *args, **kwargs):
    logger.info('save called')
    if (self.masterbudget is not None) and self.budget is None:
      self.budget = Budget.get_or_create_budget(self.masterbudget)
    if self.household is None:
      self.household = self.user.household
    record = super(Record, self).save(*args, **kwargs)

  def __str__(self):
    return '{} - {}'.format(self.name, self.amount)




