from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from pizza.models import PizzaOrder
from pizza.forms import PizzaOrderForm, DeliveryForm
from tasks import create_report


# Create your views here.


def index(request):
    if request.method == 'GET':
        pizzas = PizzaOrder.objects.all()
        return render_to_response('pizza/index.html', {'pizzas': pizzas})
    return HttpResponse(status=405)


def create(request):
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
    if request.method == 'GET':
        result = create_report.apply_async()

        return redirect(reverse('pizza:get_stats_report', kwargs={
                'task_id': result.task_id
            }))

    return HttpResponse(status=405)


@login_required
def get_stats_report(request, task_id):
    result = create_report.AsyncResult(task_id)
    if result.ready():
        params = result.get()
        return render_to_response('pizza/stats.html', {'params': params})
    else:
        return HttpResponse('Report is not ready yet, try later')
