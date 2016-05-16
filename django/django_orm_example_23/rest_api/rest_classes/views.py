# -*- coding: utf-8 -*-

from rest_framework import viewsets

from pizza.models import PizzaMenuItem
from auth_app.models import CustomUser
from rest_api.rest_classes.serializers import (
    PizzaMenuItemSerializer,
    UserSerializer,
)

__author__ = 'sobolevn'


class PizzaMenuItemViewSet(viewsets.ModelViewSet):
    """
    Menu list resource (all pizzas available at our cafe).

    """
    queryset = PizzaMenuItem.objects.all()
    serializer_class = PizzaMenuItemSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Registered user resource.

    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
