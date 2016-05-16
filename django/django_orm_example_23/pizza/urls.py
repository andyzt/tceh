from django.conf.urls import url, include

from pizza.views import create, view, close, stats, get_stats_report


urlpatterns = [
    url(r'^create/', create, name='create'),
    # view/<int:pizza_order_id>
    url(r'^view/(?P<pizza_order_id>[0-9]+)/', view, name='view'),
    url(r'^close/(?P<pizza_order_id>[0-9]+)/', close, name='close'),

    url(r'^stats/(?P<task_id>.+)/', get_stats_report, name='get_stats_report'),
    url(r'^stats/$', stats, name='stats'),
]
