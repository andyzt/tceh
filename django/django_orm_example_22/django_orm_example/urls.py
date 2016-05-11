"""django_orm_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from pizza import urls as pizza_urls
from auth_app import urls as auth_urls
from rest_api import urls as rest_urls
from pizza.views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),

    url(r'^pizza/', include(pizza_urls, namespace='pizza')),
    url(r'^users/', include(auth_urls, namespace='auth_app')),
    url(r'^api/', include(rest_urls, namespace='rest_app')),

    url(r'^$', index, name='index'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
