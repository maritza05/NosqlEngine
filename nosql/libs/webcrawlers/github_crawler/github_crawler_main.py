from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import json
import time


def getText(parent):
        return ''.join(parent.find_all(text=True, recursive=False)).strip()

def get_count_language(term, language):
    try:
        print("Term: "+ term +" Language: " + language)
        url = 'https://api.github.com/search/repositories?q=%s+language:%s&sort=stars&order=desc' %(term, language)
        print("URL: " + url)
        response = urlopen(url).read().decode('utf8')
        json_content = json.loads(response)
        return json_content['total_count']
    except:
        time.sleep(65)

def get_count_repos(term):
    try:
        url = 'https://api.github.com/search/repositories?q=%s&order=desc' %(term)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        print("URL: " + url)
        response = urlopen(req).read().decode('utf8')
        json_content = json.loads(response)
        return json_content['total_count']
    except Exception as e:
        print(e)

def get_count_for_all_languages(term):
    html = urlopen("https://github.com/search?q=%s" %(term))
    bsObj =  BeautifulSoup(html, "lxml")
    gitInfo =  bsObj.find('ul', {'class' : 'filter-list small'})
    languages = gitInfo.findAll('li')
    names = [getText(name.find('a')) for name in languages]
    counts = [lang.find('span', {'class': 'count'}).get_text() for lang in languages]
    langs = dict()
    for name, count in zip(names, counts):
        langs[name] = int(count.replace(',', ''))
    return langs