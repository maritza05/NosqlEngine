from ..webcrawlers.stackoverflow_crawlers.stackoverflow_main import StackoverflowScrapper
from .clean_data.clean_data import clean_parenthesis, clean_space_after_points


def load_description_from_stackoverflow(slug):
    try:
        stackoverflow_scrapper = StackoverflowScrapper(slug)
        description = stackoverflow_scrapper.get_tag_description()
        description = clean_parenthesis(description)
        description = clean_space_after_points(description)
        return description
    except:
        print("# Error stackoverflow description not found")
        return None