from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.nosql_list, name='nosql_list'),
    url(r'^(?P<datamodel_slug>[-\w+])/$', views.nosql_list, name='nosql_list_by_datamodel'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.nosql_detail, name='nosql_detail'),
]