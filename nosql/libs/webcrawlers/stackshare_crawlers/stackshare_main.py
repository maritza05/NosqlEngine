from bs4 import BeautifulSoup
from urllib.request import urlopen


class StackshareCrawler:

    def __init__(self, name):
        try:
            url = "http://stackshare.io/%s" %(name)
            html = urlopen(url)
            self.bsObj = BeautifulSoup(html, "lxml")
        except:
            return None

    # Get attributes
    def get_attributes(self):
        try:
            container = self.bsObj.find('div', {'id': 'service-pills-nav'})
            tab_list = container.findAll('li')
            attrs = dict()
            for info in tab_list:
                text = info.get_text()
                values = text.split('\n')
                values = [val for val in values if val]
                attr, val = values
                if val.endswith('K'):
                    val = val.replace('K', '')
                    val = float(val) * 1000
                    val = int(val)
                attrs[attr] = val
            return attrs
        except Exception as e:
            print("# Error: %s", e)
            return False

    def get_description(self):
        try:
            description = self.bsObj.find('span', {'itemprop': 'about'})
            return description.get_text()
        except:
            return False

    def get_comments(self):
        try:
            comment_cont = self.bsObj.find('td', {'class': 'reasons-list'})
            reasons = comment_cont.findAll('div', {'class': 'reason_item'})
            comments = dict()
            for reason in reasons:
                count = reason.find('span', {'class': 'reason-count'})
                text = reason.find('span', {'class': 'reason-author-pop'})
                comments[text.get_text()] = int(count.get_text())
            return comments
        except:
            return False

    def get_starts(self):
        # Get favorite
        try:
            favorite = self.bsObj.find('div', {'class': 'star-count'})
            return int(favorite.get_text())
        except:
            return False
