from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.nosql_list, name='nosql_list'),
    url(r'^(?P<datamodel_slug>[-\w]+)/$', views.nosql_list, name='nosql_list_by_datamodel'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.nosql_detail, name='nosql_detail'),

    # urls to load content
    url(r'^load/nosql/names', views.load_datamodels_and_nosqls_names, name='load_data_models_and_nosqls_names'),
    url(r'^delete/nosql/data', views.delete_all_data, name='delete_all_data'),
    url(r'^load/nosql/dbengine', views.load_all_nosql_basic, name='load_all_nosql_basic'),
    url(r'^load/github/data', views.load_github_data_for_all_nosql, name='load_all_github_data'),
    url(r'^load/drivers/github/data', views.load_drivers_for_all_nosql, name='load_drivers_for_all_nosql'),
    url(r'^load/descriptions/data', views.load_descriptions_for_all_nosql, name='load_all_descriptions'),
    url(r'^load/stackshare/data', views.get_all_stackshare_votes, name='load_stackshare_votes'),
    url(r'^load/stackoverflow/data', views.get_all_stackoverflow_followers_and_questions, name='load_stackoverflow'),

]