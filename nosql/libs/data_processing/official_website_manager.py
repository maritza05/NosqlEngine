from ..webcrawlers.official_website_crawlers.official_website_main import OfficialWebsiteCrawler
from .clean_data.clean_data import clean_space_after_points, clean_parenthesis

def get_official_description(url):
    try:
        crawler = OfficialWebsiteCrawler(url)
        raw_description = crawler.extract_text_from_official_website(url)
        clean_descr = clean_parenthesis(raw_description)
        clean_descr = clean_space_after_points(clean_descr)
        return clean_descr
    except:
        print("# Err official description not found")
        return None
