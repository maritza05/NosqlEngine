import re

def clean_description(description):
    text = description.replace('\n', '')
    text = text.replace('\xa0', '')
    return text

def clean_dates_from_comment(comment):
    regex = r"([a-zA-Z]+) (\d+), (\d+) ... "
    clean_comment = re.sub(regex, "", comment)
    return clean_comment