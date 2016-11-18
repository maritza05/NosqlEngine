import unicodedata
import urllib.parse

def remove_accents(str):
    nfkd_form = unicodedata.normalize('NFKD', str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def format_url(url):
    url = url.strip()
    url = url.replace(' ', '%20')
    url = remove_accents(url)
    return url

def clean_link(url):
    return urllib.parse.unquote_plus(url)