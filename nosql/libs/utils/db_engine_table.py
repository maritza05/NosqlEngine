from ..webcrawlers.db_engine_crawlers import db_engine_main

URL = 'url'
DEVELOPER = 'developer'
INITIAL_RELEASE = 'initial_release'
CURRENT_RELEASE = 'current_release'
LICENSE = 'license'
IMPLEMENTATION_LANGUAGE = 'implementation_language'
DATA_TYPES = 'data_types'
SYSTEMS = 'systems'
LANGUAGES = 'languages'

def get_main_info_from_source(nosql_url):
    crawler = db_engine_main.DBEngineCrawler()
    data = crawler.process_table_info(nosql_url)
    cleaned_data = dict()
    print(" **** Getting the info from the nosql: %s -> %s" %(nosql_url, str(data)))
    for attribute in data:
        if attribute['name']:
            if "Description" in attribute['name']:
                cleaned_data['description'] = attribute['description']

            if "Website" in attribute['name']:
                cleaned_data[URL] = attribute['url']

            if "Developer" in attribute['name']:
                cleaned_data[DEVELOPER] = attribute['description']

            if "Initial release" in attribute['name']:
                cleaned_data[INITIAL_RELEASE] = attribute['description']

            if "Current release" in attribute['name']:
                cleaned_data[CURRENT_RELEASE] = attribute['description']

            if "License" in attribute['name']:
                license_name = attribute.get('description_info')
                if license_name is not None:
                    cleaned_data[LICENSE] = "%s (%s)" %(attribute.get('description_info'), attribute['description'])
                else:
                    cleaned_data[LICENSE] = attribute['description']

            if "Implementation language" in attribute['name']:
                cleaned_data[IMPLEMENTATION_LANGUAGE] = attribute['description']

            if "Typing" in attribute['name']:
                data_types = attribute.get('description_info')
                if data_types:
                    cleaned_data[DATA_TYPES] = data_types
                else:
                    cleaned_data[DATA_TYPES] = attribute.get('description')

            if "Server operating systems" in attribute['name']:
                systems = attribute.get('list')
                if systems:
                    systems.append(attribute.get('description'))
                    op_systems = ', ' .join(systems)
                    cleaned_data[SYSTEMS] = op_systems
                else:
                    cleaned_data[SYSTEMS] = attribute['description']

            programming_languages = crawler.get_supported_languages(nosql_url)
            if programming_languages:
                cleaned_data[LANGUAGES] = programming_languages
        else:
            cleaned_data['description'] = attribute['description']

    return cleaned_data


if __name__ == "__main__":
    print(get_main_info_from_source('http://db-engines.com/en/system/Cubrid'))






