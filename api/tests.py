from django.test import TestCase
from .models import *

# Create your tests here.

class RecordTestCase(TestCase):
    def setUp(self):
        Household.objects.create(name='deepanju')
        User.objects.create(username='deepan')

    def test_objects_are_created(self):
        h = Household.objects.get(name='deepanju')
        user = User.objects.get(username='deepan')
        print(h.__dict__)
        print(user.__dict__)


