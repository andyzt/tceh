# -*- coding: utf-8 -*-

from datetime import timedelta
from itertools import islice

from celery.task import periodic_task, TaskSet
from django.db.models import Count, Avg
from django.utils import timezone

from django_orm_example.celery_app import app
from pizza.models import PizzaOrder, PizzaOrderNotification

__author__ = 'sobolevn'


def chunks(it, n):
    for first in it:
        yield [first] + list(islice(it, n - 1))


def _task_set_wrapper(inner_task, iterable):
    """

    :param inner_task:
    :param iterable:
    :return:
    """
    if not iterable:
        return

    tasks = (inner_task.si(chunk) for chunk in chunks(iter(iterable), 10))
    return TaskSet(tasks).apply_async()


@app.task
def create_report():
    count = PizzaOrder.objects.count()
    average_extras = PizzaOrder.objects.all().annotate(
        extra_count=Count('extra')
    ).aggregate(result=Avg('extra_count'))

    today = timezone.now()
    query = {
        'date_created__day': today.day,
        'date_created__month': today.month,
        'date_created__year': today.year,
    }
    today_pizzas = PizzaOrder.objects.filter(
        **query
    ).count()

    today_delivered = PizzaOrder.delivered_manager.filter(
        # delivered=True,  # TODO: manager
        **query
    ).count()

    # average_delivery_time = PizzaOrder.objects.filter(
    #     delivered=True,
    # ).annotate(
    #     diff=F('date_delivered') - F('date_created')
    # ).aggregate(result=Avg('diff'))

    params = {
        'count': count,
        'average_extras': average_extras['result'],
        'today_pizzas': today_pizzas,
        'today_delivered': today_delivered,
        # 'average_delivery_time': average_delivery_time,
    }

    return params

    # return render_to_response('pizza/stats.html', {'params': params})


@app.task
def send_notification(order_id):
    order = PizzaOrder.objects.get(pk=order_id)

    print('Notified!')  # TODO: do some real stuff

    notification = PizzaOrderNotification.objects.create(order=order)
    return {'notification_id': notification.id}


@app.task
def greet_new_orders():
    orders_to_notify = PizzaOrder.objects.filter(
        notifications__isnull=True,
    )  # .values_list('id', flat=True)

    # return orders_to_notify

    result = []
    for order in orders_to_notify:
        notification = PizzaOrderNotification.objects.create(order=order)
        result.append({'notification_id': notification.id})

    return result
    # TODO: see how TaskSet is better for this action:
    # _task_set_wrapper(send_notification, orders_to_notify)
