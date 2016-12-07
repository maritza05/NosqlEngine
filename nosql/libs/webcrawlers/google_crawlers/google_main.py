from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

from ...utils import url_format
class GoogleCrawler:

    def __init__(self, query):
        main_url = 'https://www.google.com/search?%s' %(query)
        main_url = url_format.format_url(main_url)
        print(main_url)
        html = urlopen(Request(main_url, headers={'User-Agent': 'Mozilla'}))
        self.bsObj = BeautifulSoup(html, "html.parser")

    def __init__(self, term_to_search, keywords):
        self.term = term_to_search
        self.keywords = keywords
        main_url = 'https://www.google.com/search?q=%s' %(term_to_search)
        main_url = url_format.format_url(main_url)
        parameters = "+"
        for keyword in keywords:
            parameters += keyword + '+'
        parameters = parameters[:-1]
        main_url += parameters
        print(main_url)
        html = urlopen(Request(main_url, headers={'User-Agent': 'Mozilla'}))
        self.bsObj = BeautifulSoup(html, "html.parser")

    def clean_link(self, link):
        link = link.replace('url?q=', '')
        ind = link.index('&sa')
        link = link[:ind]
        return link



    def get_results(self):
        info = []
        articles = self.bsObj.findAll('h3', {'class': 'r'})
        for article in articles:
            content = article.next_sibling
            link = article.find('a')
            link = self.clean_link(link.attrs['href'])
            content = content.find('span', {'class': 'st'}).get_text()
            google_section = dict()
            google_section['description'] = content
            if link.startswith('/'):
                link = link[1:]
            google_section['url'] = url_format.clean_link(link)
            info.append(google_section)
        return info

    def get_links_from_results(self):
        info = []
        articles = self.bsObj.findAll('h3', {'class': 'r'})
        for article in articles:
            link = article.find('a')
            link = self.clean_link(link.attrs['href'])
            google_section = dict()
            if link.startswith('/'):
                link = link[1:]
            google_section['url'] = url_format.clean_link(link)
            info.append(google_section)
        return info

    def get_links(self):
        data = self.get_links_from_results()
        urls = [article['url'] for article in data]
        return urls


if __name__ == "__main__":
    crawler = GoogleCrawler('mongodb', [])
    print("Number results: ")
    print(crawler.get_number_pages())