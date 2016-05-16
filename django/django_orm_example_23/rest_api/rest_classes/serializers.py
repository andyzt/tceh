# -*- coding: utf-8 -*-

from rest_framework import serializers

from auth_app.models import CustomUser
from pizza.models import PizzaMenuItem

__author__ = 'sobolevn'


class PizzaMenuItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PizzaMenuItem
        fields = ('id', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'our_note', 'favourite_pizza')

    favourite_pizza = PizzaMenuItemSerializer(required=False)
