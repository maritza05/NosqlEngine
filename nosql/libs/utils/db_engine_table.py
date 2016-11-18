from ..webcrawlers.db_engine_crawlers import db_engine_main

basic_attributes = [
    "Description",
    "Website",
    "Developer",
    "Initial release",
    "License",
    "Implementation language",
    "Typing",
    "Supported programming languages",
    "Server operating systems"
]


def get_main_info_from_source(nosql_url):
    crawler = db_engine_main.DBEngineCrawler()
    data = crawler.process_table_info(nosql_url)
    cleaned_data = dict()
    for attribute in data:
        if "Description" in attribute['name']:
            cleaned_data['description'] = attribute['description']

        if "Website" in attribute['name']:
            cleaned_data['url'] = attribute['url']

        if "Developer" in attribute['name']:
            cleaned_data['developer'] = attribute['description']

        if "Initial release" in attribute['name']:
            cleaned_data['initial_release'] = attribute['description']

        if "Current release" in attribute['name']:
            cleaned_data['current_release'] = attribute['description']

        if "License" in attribute['name']:
            license_name = attribute.get('description_info')
            if license_name is not None:
                cleaned_data['license'] = "%s (%s)" %(attribute.get('description_info'), attribute['description'])
            else:
                cleaned_data['license'] = attribute['description']

        if "Implementation language" in attribute['name']:
            cleaned_data['implementation_language'] = attribute['description']

        if "Typing" in attribute['name']:
            data_types = attribute.get('description_info')
            if data_types:
                cleaned_data['data_types'] = data_types
            else:
                cleaned_data['data_types'] = attribute.get('description')

        if "Server operating systems" in attribute['name']:
            systems = attribute.get('description_info')
            if systems:
                systems.append(attribute.get('description'))
                cleaned_data['systems'] = systems
            else:
                cleaned_data['systems'] = attribute['description']

        programming_languages = crawler.get_supported_languages(nosql_url)
        if programming_languages:
            cleaned_data['languages'] = programming_languages

    return cleaned_data








