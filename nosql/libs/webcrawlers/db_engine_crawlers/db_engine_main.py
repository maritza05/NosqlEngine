from urllib.request import urlopen
from bs4 import BeautifulSoup


class DBEngineCrawler:

    def clean_data_models(self, model_tag):
        if model_tag.find('a') is None:
            model = model_tag.contents[0]
        else:
            model = model_tag.get_text()
        return model

    def get_all_databases(self):
        try:
            url = "http://db-engines.com/en/ranking"
            html = urlopen(url)
            bsObj = BeautifulSoup(html, "lxml")
            database_names = bsObj.findAll('th', {'class': 'pad-l'})
            data_models = bsObj.findAll('th',  {'class': ['small', 'pad-r']})
            models = dict()
            for model_tag in data_models[1:]:
                model_name = self.clean_data_models(model_tag)
                models[model_name] = []

            for name_tag, model_tag in zip(database_names[1:], data_models[1:]):
                nosql = dict()
                name = name_tag.find('a')
                url = name.attrs['href']
                nosql['name'] = name.find(text=True, recursive=False)
                nosql['info_url'] = url
                model_name = self.clean_data_models(model_tag)
                models[model_name].append(nosql)
            return models
        except AttributeError:
            print("# Error reading website structure")
            return None

    def get_info_of_table(self, url):
        html = urlopen(url)
        bsObj = BeautifulSoup(html, "lxml")
        attributes = bsObj.findAll('td', {'class': 'attribute'})
        values = bsObj.findAll('td', {'class': 'value'})
        table = []
        for attr, val in zip(attributes[1:], values):
            info = dict()
            info['attribute'] = attr
            info['value'] = val
            table.append(info)
        return table

    def process_table_info(self, name):
        info = self.get_info_of_table(name)
        table = []
        for item in info:
            attr = item['attribute']
            val = item['value']
            data = dict()
            data['name'] = attr.find(text=True)
            text_info = attr.find('span')
            if text_info is not None:
                data['more_info'] = text_info.get_text()
            data['description'] = val.find(text=True)
            text_info2 = val.find('span')
            if text_info2 is not None:
                data['description_info'] = text_info2.find(text=True)
            url = val.find('a')
            if url is not None:
                data['url'] = url.attrs['href']
            if val.find('br') is not None:
                data['list'] = []
                data_list = [a.next_sibling for a in val.findAll('br')]
                for a in data_list:
                    tag = BeautifulSoup(str(a), "lxml")
                    data['list'].append(tag.get_text())
            table.append(data)
        return table

    def get_supported_languages(self, url):
        try:
            html = urlopen(url)
            bsObj = BeautifulSoup(html, "lxml")
            attrs = bsObj.findAll('td', {'class': 'attribute'})
            vals = bsObj.findAll('td', {'class': 'value'})
            list_langs = []
            for field, val in zip(attrs[1:], vals):
                if field.get_text() == "Supported programming languages":
                    text = str(val)
                    text = text.replace('<br/>', '<br>')
                    list_langs = text.split('<br>')
            languages = dict()
            for tag in list_langs:
                bsObj = BeautifulSoup(tag, "lxml")
                span = bsObj.find('span', {'class': 'infobox infobox_l'})
                info = ""
                if span:
                    info = span.get_text()
                text = bsObj.get_text()
                text = text.replace(info, '')
                languages[text] = info
            return languages
        except:
            return None


    def get_nosqls_databases(self):
	    all_databases = self.get_all_databases()
	    del all_databases['Relational DBMS']
	    return all_databases

if __name__ == "__main__":
    crawler = DBEngineCrawler()
    data = crawler.get_supported_languages('http://db-engines.com/en/system/RethinkDB')
    print(data)
