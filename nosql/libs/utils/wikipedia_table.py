from ..webcrawlers.google_crawlers import google_main
from ..webcrawlers.wikipedia_crawlers import wikipedia_main


def get_wikipedia_links(links):
    wiki_websites = []
    for link in links:
        if "en.wikipedia.org" in link:
            wiki_websites.append(link)
    return wiki_websites

def get_candidate_websites(name):
    try:
        google_crawler = google_main.GoogleCrawler(name, ['wikipedia', 'database'])
        links = google_crawler.get_links()
        wiki_links = get_wikipedia_links(links)
        print("These are the links that google get: ", wiki_links)
        return wiki_links
    except AttributeError as e:
        print("# Not results found, attribute error: ", e)
        return None

def get_wikipedia_summary(name):
    links = get_candidate_websites(name)
    if links:
        for link in links:
            wiki_crawler = wikipedia_main.WikipediaCrawler(link)
            table = wiki_crawler.extract_table()
            if table:
                print("Table found")
                print(table)
                return table
        return None



if __name__ == "__main__":
    get_wikipedia_summary('MongoDB')

