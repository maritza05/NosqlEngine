from ..webcrawlers.google_crawlers import google_advanced_search
import time
# def search_data_types(name, url):
#     # data_types = [
#     #     'string', 'integer', 'boolean', 'double',
#     #     'array', 'time', 'object', 'symbol',
#     #     'date', 'code', 'regular expression', 'numbers',
#     #     'binary', 'float', 'list', 'geometry', 'BLOB',
#     #     'data', 'types'
#     # ]
#     data_types = ['integer', 'string']
#     search_query = '%s+data+types+OR+integer+OR+string+OR+boolean+OR+float' %(name)
#     #search_query += '+OR+'.join(data_types)
#     #search_query += '+site:%s' %(url)
#
#     crawler = google_main.GoogleCrawler(search_query, [])
#     print(crawler.get_results())


def search_phrase(name):
    query = 'as_q=allintext:+"%s+performance+is"&lr=lang_en&tbs=lr:lang_1en&start=0' %(name)
    crawler = google_advanced_search.GoogleAdvancedCrawler(query)
    pages = crawler.get_number_pages()
    results = crawler.get_results()
    for i in range(2, pages+1):
        time.sleep(10)
        start = i * 10
        query = 'as_q=allintext:+"%s+performance+is"&lr=lang_en&tbs=lr:lang_1en&start=%d' %(name, start)
        results += crawler.get_results()
    return results

