from django.test import TestCase

# Create your tests here.
from pizza.models import PizzaSize


class TestPizzaSize(TestCase):
    def test_pizza_size_creation(self):
        pizza_size = PizzaSize.objects.create(size=PizzaSize.SMALL[0])
        self.assertNotEqual(pizza_size.pk, None)

