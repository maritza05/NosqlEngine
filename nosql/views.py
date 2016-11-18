from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

# Models
from .models import DataModel, Nosql

# Crawlers
from .libs.webcrawlers.db_engine_crawlers import db_engine_main

from .libs.utils import wikipedia_table
from .libs.utils import db_engine_table

from .libs.data_processing import nosql_data_manager



############## Options for admin #####################

def load_datamodels(request, datamodels_names):
    for name in datamodels_names:
        DataModel.objects.get_or_create(name=name)

def load_nosqls(request, data):
    for datamodel_name, nosqls in data.items():
        datamodel = DataModel.objects.get(name=datamodel_name)
        for nosql in nosqls:
            url = nosql['info_url']
            name = nosql['name']
            Nosql.objects.get_or_create(name=name,
                                        data_url=url,
                                        datamodel=datamodel)

def load_all_basic_data(request):
    crawler = db_engine_main.DBEngineCrawler()
    data = crawler.get_nosqls_databases()

    # Load all the datamodels first
    load_datamodels(request, data.keys())

    # Now load all the nosqls
    load_nosqls(request, data)
    return redirect('nosql:nosql_list')

def reload_all_data(request):
    # First delete the Nosqls
    Nosql.objects.all().delete()
    DataModel.objects.all().delete()
    return redirect('nosql:nosql_list')



############## Options for User ######################
def nosql_list(request, datamodel_slug=None):
    datamodel = None
    datamodels = DataModel.objects.all()
    nosqls = Nosql.objects.all()
    if datamodel_slug:
        datamodel = get_object_or_404(DataModel, slug=datamodel_slug)
        nosqls = nosqls.filter(datamodel=datamodel)
    return render(request, 'nosql_engine/nosql/list.html', {'datamodel': datamodel,
                                                      'datamodels': datamodels,
                                                      'nosqls': nosqls})

def nosql_detail(request, id, slug):
    nosql = get_object_or_404(Nosql, id=id, slug=slug)

    # Load dinamycally the Wikipedia table
    wiki_table = wikipedia_table.get_wikipedia_summary(nosql.name)

    # Load the basic info from dbengine website
    print("===> Cleaned data: ")
    basic_info = db_engine_table.get_main_info_from_source(nosql.data_url)
    nosql = nosql_data_manager.generate_fields_from_data(id, basic_info)

    return render(request, 'nosql_engine/nosql/detail.html', {'nosql': nosql,
                                                              'wiki_table': wiki_table})

