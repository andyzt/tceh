# -*- coding: utf-8 -*-

from behave import when, given, then

from pizza.models import PizzaSize, PizzaMenuItem, Address, PizzaOrder

__author__ = 'sobolevn'


@given('we have all fixtures installed')
def step_impl(context):
    assert PizzaSize.objects.exists()
    assert PizzaMenuItem.objects.exists()


@when('client orders "{menu_item}" "{size}" pizza to "{address}"')
def step_impl(context, menu_item, size, address):
    context.order_meta = {
        'menu_item': menu_item,
        'size': size,
        'address': address,
    }


@then('order is created')
def step_impl(context):
    size = PizzaSize.objects.get(size=context.order_meta['size'])
    kind = PizzaMenuItem.objects.get(name=context.order_meta['menu_item'])

    address = Address.objects.create(full=context.order_meta['address'])
    order = PizzaOrder.objects.create(
        kind=kind,
        size=size,
        delivery=address,
    )

    assert order.pk is not None
