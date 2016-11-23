from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

# Models
from .models import DataModel, Nosql, License, ProgrammingLanguage

# Crawlers
from .libs.webcrawlers.db_engine_crawlers import db_engine_main
from .libs.webcrawlers.github_crawler import github_crawler_main
from .libs.webcrawlers.stackshare_crawlers import stackshare_main
from .libs.webcrawlers.stackoverflow_crawlers import stackoverflow_main

from .libs.utils import wikipedia_table
from .libs.utils import db_engine_table

from .libs.data_processing import nosql_data_manager, google_manager, stackoverflow_manager, official_website_manager
import time


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


def load_nosql_basic_info_from_dbengine(request, id):
    nosql = Nosql.objects.get(id=id)
    basic_info = db_engine_table.get_main_info_from_source(nosql.data_url)

    url = nosql_data_manager.get_url(basic_info)
    developer = nosql_data_manager.get_developer(basic_info)
    initial_release = nosql_data_manager.get_initial_release(basic_info)
    current_release = nosql_data_manager.get_current_release(basic_info)
    license = nosql_data_manager.get_license(basic_info)
    languages = nosql_data_manager.get_languages(basic_info)
    data_types = nosql_data_manager.get_data_types(basic_info)
    systems = nosql_data_manager.get_systems(basic_info)
    impl_language = nosql_data_manager.get_implementation_language(basic_info)

    if url: nosql.official_website = url
    if developer: nosql.developer = developer
    if initial_release: nosql.initial_release = initial_release
    if current_release: nosql.current_release = current_release
    if data_types: nosql.typing = data_types
    if systems: nosql.operating_systems = systems
    if impl_language: nosql.implementation_language = impl_language

    if license:
        license.nosql = nosql
        license.save()
    if languages:
        for lang in languages:
            lang.nosql = nosql
            lang.save()
    nosql.save()
    print("Created nosql: %s, url: %s, developer: %s, systems: %s" %(nosql.name, nosql.official_website, nosql.developer, nosql.operating_systems))


def load_datamodels_and_nosqls_names(request):
    crawler = db_engine_main.DBEngineCrawler()
    data = crawler.get_nosqls_databases()
    load_datamodels(request, data.keys())
    load_nosqls(request, data)
    return redirect('nosql:nosql_list')

def load_all_nosql_basic(request):
    nosqls = Nosql.objects.all()
    for nosql in nosqls:
        load_nosql_basic_info_from_dbengine(request, nosql.id)
    return redirect('nosql:nosql_list')

# ************ Descriptions ******************
def load_descriptions(request, id):
    nosql = Nosql.objects.get(id=id)
    stack_description = stackoverflow_manager.load_description_from_stackoverflow(nosql.slug)
    official_description = official_website_manager.get_official_description(nosql.official_website)
    if stack_description is not None:
        nosql.stack_description = stack_description
    if official_description is not None:
        nosql.official_description = official_description
    nosql.save()

def load_descriptions_for_all_nosql(request):
    nosqls = Nosql.objects.all()
    for nosql in nosqls:
        load_descriptions(request, nosql.id)
    return redirect('nosql:nosql_list')

# ************* Github *******************
def load_repos_for_languages(id):
    nosql = Nosql.objects.get(id=id)
    required_drivers = ['c', 'java', 'perl', 'php', 'python', 'ruby', 'javascript']
    main_drivers = ProgrammingLanguage.objects.filter(slug__in=required_drivers, nosql=nosql)
    print("---> Main drivers: %s" %(main_drivers))
    for driver in main_drivers:
        count_repo = github_crawler_main.get_count_language(nosql.slug, driver.name)
        driver.amount_repos = count_repo
        driver.save()
        print("---> Driver nosql: %s, Driver name: %s, Driver count: %s" %(nosql.name, driver.name, driver.amount_repos))

def load_github_data_for_all_nosql(request):
    nosqls = Nosql.objects.all()
    for nosql in nosqls:
        try:
            amount = github_crawler_main.get_count_repos(nosql.slug)
            print("Amount of: %s -> %d" %(nosql.name, amount))
            nosql.amount_repos = amount
            nosql.save()
        except:
            time.sleep(80)
            continue
    return redirect('nosql:nosql_list')

def load_drivers_for_all_nosql(request):
    nosqls = Nosql.objects.all()
    for nosql in nosqls:
        try:
            load_repos_for_languages(nosql.id)
        except:
            time.sleep(80)
            continue
    return redirect('nosql:nosql_list')



def load_all_technologies_repos(request, id):
    nosql = Nosql.objects.get(id=id)
    technologies = github_crawler_main.get_count_for_all_languages(nosql.slug)
    print(technologies)
    amount = github_crawler_main.get_count_repos(nosql.slug)
    nosql.amount_repos = amount
    nosql.save()
    percentages = dict()
    total = nosql.amount_repos
    for key, values in technologies.items():
        name = key.lower()
        percentages[name] = (values * 100)/total
    print(percentages)
    return percentages

# **********************************************

def delete_all_data(request):
    # First delete all
    License.objects.all().delete()
    ProgrammingLanguage.objects.all().delete()
    Nosql.objects.all().delete()
    DataModel.objects.all().delete()
    return redirect('nosql:nosql_list')


# ************** Stackshare ***********************
def get_stackshare_followers(slug):
    stackshare_votes = 0
    stackshare = stackshare_main.StackshareCrawler(slug)
    if stackshare:
        stackshare_info = stackshare.get_attributes()
        if stackshare_info:
            if stackshare_info['Votes']:
               stackshare_votes = stackshare_info['Votes']
    return stackshare_votes

def get_all_stackshare_votes(request):
    nosqls = Nosql.objects.all()
    for nosql in nosqls:
        try:
            votes = get_stackshare_followers(nosql.slug)
            nosql.stackshare_votes = votes
            nosql.save()
        except:
            print("---Exception getting the info for: %s" %(nosql.slug))
            continue
    return redirect('nosql:nosql_list')

# *************** Stackoverflow *************************
def get_all_stackoverflow_followers_and_questions(request):
    nosqls = Nosql.objects.all()
    for nosql in nosqls:
         try:
            followers, questions = stackoverflow_main.get_followers(nosql.slug)
            nosql.stackoverflow_followers = int(followers)
            nosql.amount_stackoverflow_questions = int(questions)
            nosql.save()
            print("%s followers: %s, questions: %s" %(nosql.slug, nosql.stackoverflow_followers, nosql.amount_stackoverflow_questions))
         except Exception as e:
            print("# Error: %s" %(e))
            continue
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

    license = License.objects.get(nosql=nosql)
    license_type = license.get_type()
    languages = ProgrammingLanguage.objects.filter(nosql=nosql)


    print("=== Stackoverflow ")
    print(nosql.stack_description)
    print("=== Official")
    print(nosql.official_description)
    print("==== Drivers")
    load_all_technologies_repos(request, id)


    return render(request, 'nosql_engine/nosql/detail.html', {'nosql': nosql,
                                                              'license': license,
                                                              'summary': nosql.get_summary(),
                                                              'license_type': license_type,
                                                              'languages': languages,
                                                              'wiki_table': wiki_table})

