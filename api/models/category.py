from django.db import models


class Category(models.Model):
  name = models.CharField(max_length=200)
  household = models.ForeignKey('Household', null=True, blank=True)
  # consider have user and type:personal/household here

  def __str__(self):
    return self.name
