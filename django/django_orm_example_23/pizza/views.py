""" Views module
"""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from pizza.models import PizzaOrder
from pizza.forms import PizzaOrderForm, DeliveryForm
from pizza.tasks import create_report


# Create your views here.


def index(request):
    """
    This view renders the main page, listing all orders.
    Every link in the list points to the :func:`create`

    Args:
        request: HttpRequest, accepted methods: GET

    Returns:
        HttpResponse with rendered view or error with status code 405 if used another method (not GET)
    """
    if request.method == 'GET':
        pizzas = PizzaOrder.objects.all()
        return render_to_response('pizza/index.html', {'pizzas': pizzas})
    return HttpResponse(status=405)


def create(request):
    """
    This view renders a form for creating new :class:`PizzaOrder`
    or accepts POST requests with the form to save its data. Or render errors.

    PizzaOrder: is a base class that contains all order data, see field list below:

    - kind
    - size
    - delivery
    - extra
    - exclude
    - comment
    - delivered
    - date_created
    - date_delivered

    Args:
        request: HttpRequest, accepted methods: GET, POST

    Returns:
        HttpResponse with rendered view, or error code if used method other than GET or POST
    """
    if request.method == 'GET':
        c = RequestContext(request, {
            'pizza_form': PizzaOrderForm(),
            'delivery_form': DeliveryForm(),
        })
        return render_to_response('pizza/create.html', c)

    elif request.method == 'POST':
        pizza_form = PizzaOrderForm(request.POST)
        delivery_from = DeliveryForm(request.POST)

        if pizza_form.is_valid() and delivery_from.is_valid():
            user = request.user
            user = user if user.is_authenticated() else None
            with transaction.atomic():
                delivery = delivery_from.save(user=user)
                pizza = pizza_form.save(delivery=delivery)
                pizza_form.save_m2m()

            return redirect(reverse('pizza:view', kwargs={
                'pizza_order_id': pizza.pk
            }))
        else:
            c = RequestContext(request, {
                'pizza_form': pizza_form,
                'delivery_form': delivery_from,
            })
            return render_to_response('pizza/create.html', c)
    return HttpResponse(status=405)


def view(request, pizza_order_id):
    """
    This view shows us particular pizza order details (usually we can get here by link from orders page)
    Also select from related tables is performed (to show chosen values for this order)

    Args:
        request: HttpRequest, accepted methods: GET
        pizza_order_id: Integer, id of particular pizza order.
    Returns:
        HttpResponse with rendered view or errors:
        with status code 404 if order with provided id is not found
        with status code 405 if used another method (not GET)
    """
    if request.method == 'GET':
        # pizza = get_object_or_404(PizzaOrder, id=pizza_order_id)
        try:
            pizza = PizzaOrder.objects.select_related(
                'size',
                'kind',
                'delivery',
            ).prefetch_related(
                'extra',
                'exclude',
                'kind__ingredients',
            ).get(
                id=pizza_order_id
            )
        except PizzaOrder.DoesNotExist:
            raise Http404('Selected pizza not found')

        return render_to_response('pizza/view.html', {'pizza': pizza})
    return HttpResponse(status=405)


def close(request, pizza_order_id):
    """
    This view closes particular pizza order when pizza is delivered.
    After mark pizza as delivered this view redirects us to pizza:view

    Args:
        request: HttpRequest, accepted methods: GET
        pizza_order_id: Integer, id of particular pizza order.
    Returns:
        HttpResponse with redirect to pizza:view or errors:
        with status code 404 if order with provided id is not found
        with status code 405 if used another method (not GET)
    """
    if request.method == 'GET':
        try:
            pizza = get_object_or_404(PizzaOrder, id=pizza_order_id)
            pizza.mark_delivered()

            return redirect(reverse('pizza:view', kwargs={
                'pizza_order_id': pizza.pk
            }))
        except PizzaOrder.DoesNotExist:
            return HttpResponse('Does not exist', status_code=404)
    return HttpResponse(status=405)


@login_required
def stats(request):
    """
    This view creates an async task to collect various statistics about
    the created orders. As a result returns an HttpResponse with task's id.

    :param request: HttpRequest, allowed methods: GET
    :returns: HttpResponse with task's id or error if used method other than GET
    """
    if request.method == 'GET':
        response = create_report.delay()
        return HttpResponse(response.task_id)
    return HttpResponse(status=405)


@login_required()
def get_stats_report(request, task_id):
    """
    This view shows various statistics about the created orders.
    It should be called after collection task is finished.

    Args:
        request: HttpRequest, accepted methods: GET
        task_id: Integer, id of async task that is started by pizza:stats to collect statistics.
    Returns:
        HttpResponse with rendered view or errors:
        with status code 404 if task with provided id is not found
        with status code 405 if used another method (not GET)
    """
    return HttpResponse('')
