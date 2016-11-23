import requests
from nltk import word_tokenize
from math import ceil
import operator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.nlp.stemmers import Stemmer

def parseText(text):
    LANGUAGE = "english"
    SENTENCES_COUNT = 6
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizerEd = EdmundsonSummarizer(stemmer)
    summarizerEd.bonus_words = ('scalable', 'performance', 'license', 'written',
                               'querying', 'queried', 'language', 'languages',
                               'availability', 'replication', 'is', 'schema',
                                'latency', 'scales', 'data', 'caching', 'persistent')

    summarizerEd.stigma_words = ('questions', 'more', 'see', 'groups', 'help',
                                'check', 'information', 'events', 'related',
                                'download', 'us', 'come', 'workshop', 'install',
                                'discover', 'find', 'see', 'understand',
                                'example', 'ask', 'mailing', 'copyright', 'github', 'twitter', 'email')

    summarizerEd.null_words = ('also', 'compatible', 'nosql', 'NoSQL')
    sents = [str(sent) for sent in summarizerEd(parser.document, SENTENCES_COUNT)]
    summary = ' '.join(sents)
    return summary