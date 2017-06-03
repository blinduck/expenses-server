from django.db import models


class Category(models.Model):
  CAT_TYPES = (
    ("Personal","Personal"),
    ("Household","Household"),
  )

  name = models.CharField(max_length=200)
  household = models.ForeignKey('Household', null=True, blank=True)
  cat_type = models.CharField(default="Personal", choices=CAT_TYPES, max_length=100)
  user = models.ForeignKey('User', null=True, blank=True)


  def __str__(self):
    return self.name
