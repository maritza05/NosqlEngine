from django.shortcuts import render, get_object_or_404

# Models
from .models import DataModel, Nosql

def nosql_list(request, datamodel_slug=None):
    datamodel = None
    datamodels = DataModel.objects.all()
    nosqls = Nosql.objects.all()
    if datamodel_slug:
        datamodel = get_object_or_404(DataModel, slug=datamodel_slug)
        nosqls = nosqls.filter(datamodel=datamodel)
    return render(request), 'nosql/list.html', {'datamodel': datamodel,
                                                      'datamodels': datamodels,
                                                      'nosqls': nosqls}

def nosql_detail(request, id, slug):
    nosql = get_object_or_404(Nosql, id=id, slug=slug)
    return render(request, 'nosql/detail.html', {'nosql': nosql})
