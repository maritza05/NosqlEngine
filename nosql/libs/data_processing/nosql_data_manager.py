from django.core.exceptions import ObjectDoesNotExist

from ...models import Nosql


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
                nosql.license = value
            if 'implementation_language' in key:
                nosql.implementation_language = value
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


