from urllib.request import urlopen
from bs4 import BeautifulSoup


class WikipediaCrawler:

    def __init__(self, url):
        html = urlopen(url)
        self.bsObj = BeautifulSoup(html, "html.parser")


    def extract_table(self):
        try:
            table = self.bsObj.find("table", {"class": "infobox vevent"})
            rows = table.findAll("tr")
            data = dict()
            for row in rows:
                if row.th is not None:
                   attribute = row.th.get_text()
                   value = row.td.get_text()
                   data[attribute] = value
            return data
        except AttributeError:
            print("# The link exists but there isn't table in the website")
            return None


if __name__ == "__main__":
    wiki = WikipediaCrawler('Redis')
    wiki.extract_license_from_table()