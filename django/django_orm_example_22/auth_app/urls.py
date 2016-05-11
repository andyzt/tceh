from django.conf.urls import url, include
from django.contrib.auth.views import login, logout_then_login

from auth_app.views import register

urlpatterns = [
    url(r'^login/', login, {
        'template_name': 'auth_app/login.html',
    }, name='login'),
    url(r'^logout/', logout_then_login, name='logout'),
    url(r'^register/', register, name='register'),
]
