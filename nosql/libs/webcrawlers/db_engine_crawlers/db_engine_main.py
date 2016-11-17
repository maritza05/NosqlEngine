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

    def get_nosqls_databases(self):
	    all_databases = self.get_all_databases()
	    del all_databases['Relational DBMS']
	    return all_databases