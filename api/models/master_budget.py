from django.db import models


class MasterBudget(models.Model):
    PERIOD_CHOICES = (
        ('Monthly', 'Monthly'),
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
    user = models.ForeignKey('User')
    period = models.CharField(max_length=50, choices=PERIOD_CHOICES, default='Monthly')
    expense_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Personal')

    def __str__(self):
        return self.name
