from django.core.exceptions import ObjectDoesNotExist

from ...models import Nosql, License, ProgrammingLanguage
from ..utils import db_engine_table


def process_license(data):
    if data.find("(") != -1:
        type = data[data.find("(")+1: data.find(")")]
        type = type.strip()
        name = data[:data.find("(")]
        name = name.strip()
    else:
        type = data
        name = None
    return type, name

def get_url(data):
    return data.get(db_engine_table.URL, None)

def get_developer(data):
    return data.get(db_engine_table.DEVELOPER, None)

def get_initial_release(data):
    return data.get(db_engine_table.INITIAL_RELEASE, None)

def get_current_release(data):
    return data.get(db_engine_table.CURRENT_RELEASE, None)

def get_license(data):
    license = data.get(db_engine_table.LICENSE, None)
    if license:
        type, name = process_license(license)
        license_obj = License()
        if name:
            license_obj.name = name
        if 'open source' in type.lower():
            license_obj.open_source_type = True
        if 'free' in type.lower():
            license_obj.free_type = True
        if 'commercial' in type.lower():
            license_obj.commercial_type = True
        license_obj.undefined_type = False
        license_obj.save()
        return license_obj
    else:
        return None


def get_languages(data):
    languages = data.get(db_engine_table.LANGUAGES, None)
    print("== LANGUAGES ==")
    print(languages)
    if languages:
        clean_languages = []
        for name, type in languages.items():
            language = ProgrammingLanguage(name=name)
            status = ProgrammingLanguage.UNDEFINED
            if 'official' in type.lower():
                status = ProgrammingLanguage.OFFICIAL
            if 'community-supported' in type.lower():
                status = ProgrammingLanguage.COMMUNITY_SUPPORTED
            if 'inofficial' in type.lower():
                status = ProgrammingLanguage.INNOFICIAL
            language.status = status
            language.save()
            clean_languages.append(language)
        return clean_languages
    else:
        return None

def get_data_types(data):
    return data.get(db_engine_table.DATA_TYPES, None)

def get_systems(data):
    return data.get(db_engine_table.SYSTEMS, None)

def get_implementation_language(data):
    return data.get(db_engine_table.IMPLEMENTATION_LANGUAGE, None)



def generate_fields_from_data(id, data):
    try:
        nosql = Nosql.objects.get(id=id)
        for key, value in data.items():
            if 'url' in key:
                nosql.official_website = value
            if 'developer' in key:
                nosql.developer = value
            if 'initial_release' in key:
                nosql.initial_release = value
            if 'current_release' in key:
                nosql.current_release = value

            if 'license' in key:
                type, name = process_license(value)
                license = License(name=name)
                if 'open source' in type.lower():
                    license.open_source_type = True
                if 'free' in type.lower():
                    license.free_type = True
                if 'commercial' in type.lower():
                    license.commercial_type = True
                license.nosql = nosql
                license.save()

            if 'languages' in key:
                for name, type in value.items():
                    name = name.strip()
                    language = ProgrammingLanguage(name=name)
                    if 'official' in type.lower():
                        language.status = ProgrammingLanguage.OFFICIAL
                    if 'community-supported' in type.lower():
                        language.status = ProgrammingLanguage.COMMUNITY_SUPPORTED
                    if 'inofficial' in type.lower():
                        language.status = ProgrammingLanguage.INNOFICIAL
                    language.nosql = nosql
                    language.save()

            if 'data_types' in key:
                nosql.typing = value
            if 'systems' in key:
                nosql.operating_systems = value
            if 'languages' in key:
                nosql.supported_programming = value
            if 'implementation_language' in key:
                nosql.implementation_language = value
        nosql.save()
        return nosql

    except ObjectDoesNotExist:
        print("Not nosql found with that ID")


