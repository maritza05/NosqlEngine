import elasticsearch_dsl
import elasticsearch_dsl.connections

from django.core.management import BaseCommand

from ...models import Nosql, ProgrammingLanguage, License
from ...es_docs import ESNosql

class Command(BaseCommand):
    help = "Index all data to Elasticsearch"

    def handle(self, *args, **options):
        elasticsearch_dsl.connections.connections.create_connection()
        ESNosql.init(index='nosqlengine')
        for nosql in Nosql.objects.all():
            print("Nosql: %s" %(nosql.name))
            esn = ESNosql(meta={'id': nosql.id},
                          name=nosql.name, slug=nosql.slug, data_url=nosql.data_url,
                          official_website=nosql.official_website, developer=nosql.developer,
                          initial_release=nosql.initial_release, current_release=nosql.current_release,
                          implementation_language=nosql.implementation_language, typing=nosql.typing,
                          operating_systems=nosql.operating_systems,
                          stack_description=nosql.stack_description,
                          official_description=nosql.official_description, amount_repos=nosql.amount_repos,
                          stackshare_votes=nosql.stackshare_votes, stackoverflow_followers=nosql.stackoverflow_followers,
                          amount_stackoverflow_questions=nosql.amount_stackoverflow_questions,
                          datamodel=nosql.datamodel.name, rank=nosql.get_rank(),
                          local_website=nosql.get_absolute_url())

            for pl in ProgrammingLanguage.objects.filter(nosql=nosql):
                esn.programming_languages.append(pl.name)

            for lc in License.objects.filter(nosql=nosql):
                esn.licenses.append(lc.get_type())
            esn.save(index='nosqlengine')


