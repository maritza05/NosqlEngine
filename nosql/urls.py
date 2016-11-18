from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.nosql_list, name='nosql_list'),
    url(r'^(?P<datamodel_slug>[-\w]+)/$', views.nosql_list, name='nosql_list_by_datamodel'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.nosql_detail, name='nosql_detail'),

    # urls to load content
    url(r'^load/nosql/basic', views.load_all_basic_data, name='load_basic_data'),
    url(r'^reload/nosql/data', views.reload_all_data, name='reload_all_data')
]