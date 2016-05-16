from django.test import TestCase
from pizza.models import PizzaSize

class TestPizzaSize(TestCase):
#     def setUp(self):
#        Animal.objects.create(name="lion", sound="roar")
#        Animal.objects.create(name="cat", sound="meow")

     def test_pizza_size_creation(self):
        try:
            pizza_size = PizzaSize.objects.create(size='Medium')
            self.assertNotEqual(pizza_size.pk, None)
            self.assertEqual(pizza_size.size,'Medium')
        except:
            assert False

        try:
            pizza_size = PizzaSize.objects.create(size='Giant')
            assert False
        except:
            assert True

        #models

        #views - check urls
        #templates check
        #selenium

