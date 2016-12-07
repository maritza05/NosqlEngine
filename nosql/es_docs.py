from elasticsearch_dsl import DocType
from elasticsearch_dsl import String
from elasticsearch_dsl import Long

class ESNosql(DocType):
    name = String(required=True)
    slug = String(required=True)
    data_url = String()
    official_website = String()
    local_website = String()
    developer = String()
    initial_release = String()
    current_release = String()
    implementation_language = String()
    typing = String()
    operating_systems = String()
    stack_description = String()
    official_description = String()
    amount_repos = Long()
    stackshare_votes = Long()
    stackoverflow_followers = Long()
    amount_stackoverflow_questions = Long()
    rank = Long()

    datamodel = String(required=True, index="not_analyzed")
    programming_languages = String(multi=True)
    licenses = String(multi=True)

    class Meta:
        doc_type = 'nosqls'

