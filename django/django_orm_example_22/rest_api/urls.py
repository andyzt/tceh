# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from rest_framework import routers

from rest_api.rest_classes.views import UserViewSet, PizzaMenuItemViewSet

__author__ = 'sobolevn'


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'pizzamenuitem', PizzaMenuItemViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
