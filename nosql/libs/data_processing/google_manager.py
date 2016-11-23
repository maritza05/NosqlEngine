from ..webcrawlers.google_crawlers import google_main

def search_data_types(name, url):
    # data_types = [
    #     'string', 'integer', 'boolean', 'double',
    #     'array', 'time', 'object', 'symbol',
    #     'date', 'code', 'regular expression', 'numbers',
    #     'binary', 'float', 'list', 'geometry', 'BLOB',
    #     'data', 'types'
    # ]
    data_types = ['integer', 'string']
    search_query = '%s+data+types+OR+integer+OR+string+OR+boolean+OR+float' %(name)
    #search_query += '+OR+'.join(data_types)
    #search_query += '+site:%s' %(url)

    crawler = google_main.GoogleCrawler(search_query, [])
    print(crawler.get_results())