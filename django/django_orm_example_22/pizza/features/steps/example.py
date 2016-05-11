# -*- coding: utf-8 -*-

from behave import when, given, then

__author__ = 'sobolevn'


@given('we have behave installed')
def step_impl(context):
    assert when is not None


@when('we implement {name}')
def step_impl(context, name):
    assert str(name) == name


@then('behave will test it for us')
def step_impl(context):
    assert context.failed is False
