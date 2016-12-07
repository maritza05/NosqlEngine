from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect

from elasticsearch_dsl import Search, Q

# Models
from .models import DataModel, Nosql, License, ProgrammingLanguage, Link, Comment

# Forms
from .forms import SearchForm

# Crawlers
from .libs.webcrawlers.db_engine_crawlers import db_engine_main
from .libs.webcrawlers.github_crawler import github_crawler_main
from .libs.webcrawlers.stackshare_crawlers import stackshare_main
from .libs.webcrawlers.stackoverflow_crawlers import stackoverflow_main
from .libs.webcrawlers.google_crawlers import custom_search_engine_crawler
from .libs.data_processing.clean_data import google_cleaner

from .libs.utils import wikipedia_table
from .libs.utils import db_engine_table

from .libs.paginator import custom_paginator

from .libs.data_processing import nosql_data_manager, google_manager, stackoverflow_manager, official_website_manager
from .libs.data_processing import link_rank

from .libs.sentiment_classifier.performance_classifier import PerformanceClassifier
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
        if driver.amount_repos == 0:
            count_repo = github_crawler_main.get_count_language(nosql.slug, driver.slug)
            print("Count for the repo {%s}: %d" %(driver.name, count_repo))
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


def get_stackoverflow_links(id):
    nosql = Nosql.objects.get(id=id)
    crawler = stackoverflow_main.StackoverflowScrapper(nosql.slug)
    stack_links = crawler.get_links()
    if stack_links:
        url_ranker = link_rank.UrlRank()
        for link in stack_links:
            try:
                rank = url_ranker.get_rank_of_link(link['url'])
                link_obj, created = Link.objects.get_or_create(title=link['title'], url=link['url'], nosql=nosql, number_backlinks=int(rank))
                print("Link {%s}: %d" %(link_obj.title, link_obj.number_backlinks))
                time.sleep(14)
            except Exception as e:
                print("# Error: %s" %(e))
                continue
    else:
        return None

# *************** Google ********************************
def load_comments(request):
    nosql_list = Nosql.objects.all()
    save_comments(nosql_list)
    return render(redirect('nosql:nosql_list'))



def save_comments(nosql_list):
    classifier = PerformanceClassifier()
    for nosql in nosql_list:
        actual_comments = Comment.objects.filter(nosql=nosql)
        if len(actual_comments) == 0:
            try:
                comments = google_manager.search_phrase(nosql.slug)
                for comment in comments:
                    body = comment['description']
                    label, prob = classifier.classify(body)
                    positive = (label == 1)
                    comment, created = Comment.objects.get_or_create(url=comment['url'],
                                                                     body=comment['description'],
                                                                     nosql=nosql,
                                                                     positive=positive,
                                                                     probability=prob*100)
                    if created:
                        print("Comment created: %s, %s" %(comment.body, comment.positive))
            except:
                continue

def save_comment(id):
    nosql = Nosql.objects.get(id=id)
    classifier = PerformanceClassifier()
    actual_comments = Comment.objects.filter(nosql=nosql)
    if len(actual_comments) == 0:
        try:
            crawler = custom_search_engine_crawler.CustomSearchEngine()
            comments = crawler.iterate_pages("%s+performance+is" %(nosql.slug), 4)
            for comment in comments:
                body = comment['description']
                clean_date = google_cleaner.clean_dates_from_comment(body)
                description = google_cleaner.clean_description(clean_date)
                label, prob = classifier.classify(body)
                positive = (label == 1)
                comment, created = Comment.objects.get_or_create(url=comment['url'],
                                                                     body=comment['description'],
                                                                     nosql=nosql,
                                                                     positive=positive,
                                                                     probability=prob)
                if created:
                    print("Comment created: %s, %s" %(comment.body, comment.positive))
        except Exception as e:
            print("#Error %s", e)

# *************** Formulary ******************************

def search_results(request):
    models_names = request.POST.getlist('datamodel')
    language_names = request.POST.getlist('driver')
    licenses = request.POST.getlist('license')
    name = request.POST.get('name')
    min_rank = int(request.POST.get('min_rank','0'))
    max_rank = int(request.POST.get('max_rank','0'))

    request.session['models_names'] = models_names
    request.session['language_names'] = language_names
    request.session['licenses'] = licenses
    request.session['name'] = name
    #request.session['min_rank'] = min_rank
    #request.session['max_rank'] = max_rank

    print("# Model names %s" %(models_names))
    print("# Drivers names %s" %(language_names))
    print("# Licenses %s" %(licenses))
    return HttpResponseRedirect(reverse('nosql:output_form'))


def output_form(request):
    models_names = request.session['models_names']
    language_names = request.session['language_names']
    licenses = request.session['licenses']
    name = request.session['name']
    #min_rank = request.session['min_rank']
    #max_rank = request.session['max_rank']

    page = int(request.GET.get('page', '1'))
    print("Page: %d" %(page))
    start = (page-1) * 9
    end = start + 9

    if name:
        s = Search(index="nosqlengine").query("match", name=name)
    else:
        s = Search(index="nosqlengine")

    # if min_rank != 0 and max_rank != 0:
    #     rank_query = dict()
    #     if min_rank is not None:
    #         rank_query['gte'] = min_rank
    #     if max_rank is not None:
    #         rank_query['lte'] = max_rank
    #     s = s.query('range', rank=rank_query)

    query_list_model = []
    for model in models_names:
        query_list_model.append(Q('match', datamodel=model))
    q_model = Q('bool', should=query_list_model, minimum_should_match=1)
    s = s.query(q_model)

    query_list_language = []
    for language in language_names:
        query_list_language.append(Q('match', programming_languages=language))
    q_language = Q('bool', should=query_list_language, minimum_should_match=1)
    s = s.query(q_language)

    query_list_license = []
    for license in licenses:
        query_list_license.append(Q('match', licenses=license))
    q_license = Q('bool', should=query_list_license, minimum_should_match=1)
    s = s.query(q_license)

    result = s[start:end].execute()
    print("Total: %s" %(result.hits.total))


    number_pages = int(result.hits.total / 9)
    if (result.hits.total % 9) > 0:
        number_pages += 1
    pages = range(1, number_pages+1)
    paginator = custom_paginator.DSEPaginator(result, 9)
    try:
        nosqls = paginator.page(page)
    except PageNotAnInteger:
        nosqls = paginator.page(1)
    except EmptyPage:
        nosqls = paginator.page(paginator.num_pages)

    ids = [nosql.slug for nosql in nosqls]
    nosqls = Nosql.objects.filter(slug__in=ids)
    for nosql in nosqls:
        save_comment(nosql.id)

    datamodels = DataModel.objects.all()
    languages = ['C', 'java', 'perl', 'php', 'python', 'ruby', 'javascript']
    licenses = ['Commercial', 'Open Source', 'Free']

    return render(request, 'remark_theme/material_menu.html', {'nosqls': nosqls,
                                                                'datamodels': datamodels,
                                                               'languages': languages,
                                                            'licenses': licenses,
                                                            'pages': pages})



############## Options for User ######################

def nosql_list(request, datamodel_slug=None):
    datamodel = None
    datamodels = DataModel.objects.all()
    languages = ['C', 'java', 'perl', 'php', 'python', 'ruby', 'javascript']
    licenses = ['Commercial', 'Open Source', 'Free']
    nosqls = Nosql.objects.all()
    if datamodel_slug:
        datamodel = get_object_or_404(DataModel, slug=datamodel_slug)
        nosqls = nosqls.filter(datamodel=datamodel)
    paginator = Paginator(nosqls, 9)
    page = request.GET.get('page')
    try:
        nosqls = paginator.page(page)
    except PageNotAnInteger:
        nosqls = paginator.page(1)
    except EmptyPage:
        nosqls = paginator.page(paginator.num_pages)

    return render(request, 'remark_theme/material_menu.html', {'datamodel': datamodel,
                                                      'datamodels': datamodels,
                                                      'nosqls': nosqls,
                                                            'languages': languages,
                                                            'licenses': licenses})

def nosql_detail(request, id, slug):
    nosql = get_object_or_404(Nosql, id=id, slug=slug)

    # Load dinamycally the Wikipedia table
    wiki_table = wikipedia_table.get_wikipedia_summary(nosql.name)
    print("Wiki! %s" %(wiki_table))

    license = License.objects.get(nosql=nosql)
    license_type = license.get_type()


    print("=== Stackoverflow ")
    print(nosql.stack_description)
    print("=== Official")
    print(nosql.official_description)
    print("==== Drivers")

    import operator
    technologies = load_all_technologies_repos(request, id)
    sorted_x = sorted(technologies.items(), key=operator.itemgetter(1), reverse=True)

    # load stackoverflow links if the nosql doesnt have one
    if not Link.objects.filter(nosql=nosql):
        get_stackoverflow_links(nosql.id)
    links = Link.objects.filter(nosql=nosql)

    load_repos_for_languages(nosql.id)
    languages = ProgrammingLanguage.objects.filter(nosql=nosql)

    save_comment(nosql.id)
    comments = Comment.objects.filter(nosql=nosql)
    data_types = nosql.typing.split(',')
    performance_e = nosql.get_performance_ranking()

    required_drivers = ['c', 'java', 'perl', 'php', 'python', 'ruby', 'javascript']
    main_drivers =ProgrammingLanguage.objects.filter(slug__in=required_drivers, nosql=nosql)

    same_model = Nosql.objects.filter(datamodel=nosql.datamodel).exclude(id=nosql.id)[:5]
    more_popular = Nosql.objects.all().exclude(id=nosql.id)[:5]
    buckets = nosql.get_ranking_distribution()

    good_performance = sorted(Nosql.objects.all(), key= lambda n: n.get_performance_rank()[0])
    good_performance = good_performance[:6]
    print("****Comments: %s" %(nosql.get_comments()))






    return render(request, 'remark_theme/summary_version2.html', {'nosql': nosql,
                                                              'license': license,
                                                              'summary': nosql.get_summary(),
                                                              'license_type': license_type,
                                                              'languages': languages,
                                                              'links': links,
                                                                  'good_performance': good_performance,
                                                              'comments': comments,
                                                                  'more_popular': more_popular,
                                                                  'same_model': same_model,
                                                                  'main_drivers': main_drivers,
                                                                  'datatypes': data_types,
                                                                  'evaluation': performance_e,
                                                                  'drivers': languages,
                                                                  'technologies': sorted_x,
                                                                  'buckets': buckets,
                                                              'wiki_table': wiki_table
                                                              })

