from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import nltk
import string

class OfficialWebsiteCrawler:

    def __init__(self, main_url):
        self.main_url = main_url
        html = urlopen(Request(self.main_url, headers={'User-Agent': 'Mozilla'}))
        self.bsObj = BeautifulSoup(html, "html.parser")


    def extract_text_from_official_website(self, page_name):
        raw_text = self.bsObj.findAll("p")
        clean_text = ""
        for text in raw_text:
            clean_text += text.get_text().strip(' ')
        words = nltk.word_tokenize(clean_text)
        text = ''.join([('' if c in string.punctuation else ' ')+ c for c in words]).strip()
        return text