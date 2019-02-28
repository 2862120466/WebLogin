from django.conf.urls import url
from . import views
from .models import User

urlpatterns = [
    url('^$',views.main),
    url('^index/$',views.index),
    url('^login/$',views.login),
    url('^register/$',views.register),
    url('^logout/$',views.logout),
    url(r'^confirm/$', views.user_confirm),
]